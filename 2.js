const Log = require('./Logger')
const logger = Log.getLogger('taskList_listener');
const axios = require('axios')
const path = require('path')
const qs = require('qs');
const fs = require('fs')
const adsHost = 'http://local.adspower.net:50325'
const puppeteer = require('puppeteer');
const { json } = require('express');
const { execSync } = require('child_process');
const { error, Console } = require('console');
let isExecuting = false; // 用于标记是否请求正在进行中
let queue = []; // 队列来保存需要执行的请求
let maxBrowserScheduler = 1c
const jsFilePath = path.resolve(__dirname, 'shein_2.js');
// 获取本地图片的绝对路径
const localImagePath = path.resolve(__dirname, '1.png');
// 读取本地图片文件
const imageBuffer = fs.readFileSync(localImagePath);

const cacheableTypes = ['script', 'stylesheet', 'font'];
const jsContent = fs.readFileSync(jsFilePath, 'utf8');
let stringArray = ["1130_900", "1152_864", "1280_720",  "1024_768", "1280_800"]
let allResults = {}

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms)); // 延迟函数
}
function imageToBase64(filepath) {
    const imageData = fs.readFileSync(filepath); // 读取图片的二进制数据
    const base64Data = Buffer.from(imageData).toString('base64'); // 转换为 Base64
    return base64Data;
}
let UGGBrowser = null

function getRandomString(length) {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let result = '';
    for (let i = 0; i < length; i++) {
        result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return result;
}

// 锁的状态
let isLocked = false;



// 创建一个简单的锁
function acquireLock() {
    return new Promise((resolve) => {
        const checkLock = () => {
            if (!isLocked) {
                isLocked = true; // 锁定
                resolve();       // 继续执行
            } else {
                setTimeout(checkLock, 100); // 如果锁住了，等待100毫秒后再检查
            }
        };
        checkLock();
    });
}

// 释放锁
function releaseLock() {
    isLocked = false;
}
const { exec } = require('child_process');


async function runPy2(foot) {
    try {
        console.log('Running:', foot);
        const result = await new Promise((resolve, reject) => {
            exec(foot, { encoding: 'utf-8', windowsHide: true, timeout: 120000 }, (error, stdout, stderr) => {
                if (error) {
                    if (error.killed && error.signal === 'SIGTERM') {
                        reject(new Error("Process timed out and was killed"));
                    } else {
                        reject(error);
                    }
                } else {
                    resolve(stdout);
                }
            });
        });
        console.log('Result:', result);
    } catch (error) {
        console.error('Error during execution:', error);
    }
}

async function runPy(foot) {
    
    if(foot.includes('ugg') && !foot.includes('start')) {
        console.log('不需要锁')
    }else {
        await acquireLock();  // 获取锁
    }
    try {
        console.log('Running:', foot);
        const result = await new Promise((resolve, reject) => {
            exec(foot, { encoding: 'utf-8', windowsHide: true, timeout: 120000 }, (error, stdout, stderr) => {
                if (error) {
                    if (error.killed && error.signal === 'SIGTERM') {
                        reject(new Error("Process timed out and was killed"));
                    } else {
                        reject(error);
                    }
                } else {
                    resolve(stdout);
                }
            });
        });
        console.log('Result:', result);
    } catch (error) {
        console.error('Error during execution:', error);
    } finally {
        releaseLock();  // 释放锁
    }
}

function startBrowserAndProcess(url, vendor, res, images) {
    return new Promise(async (resolve, reject) => {
        try {
            logger.info(`浏览器启动成功 端口:${res.data.data.debug_port}`);
            let puppeteerUrl = res.data.data.ws.puppeteer;
            logger.info(`浏览器启动成功 puppeteerUrl: ${puppeteerUrl}`);

            // 连接到浏览器
            const browser = UGGBrowser || await puppeteer.connect({
                browserWSEndpoint: puppeteerUrl,
                defaultViewport: null
            });

            // 获取页面
            const pages = await browser.pages();
            const page = pages[0];

            // 删除现有的图片文件
            let imageCount = 0;
            const filePath = `${vendor}_intercepted_image.png`;
            const filePath2 = `${vendor}_intercepted_image.jpg`;


            try {
                // 检查并删除文件
                if (fs.existsSync(filePath)) {
                    fs.unlinkSync(filePath);
                    console.log(`File ${filePath} deleted successfully.`);
                } else {
                    console.log(`File ${filePath} does not exist.`);
                }
                if (fs.existsSync(filePath2)) {
                    fs.unlinkSync(filePath2);
                    console.log(`File ${filePath2} deleted successfully.`);
                } else {
                    console.log(`File ${filePath2} does not exist.`);
                }
            } catch (err) {
                console.error(`Error deleting files:`, err);
                return reject(err);
            }

            // 拦截图片响应
            page.on('response', async (response) => {
                const url = response.url();
                // 只拦截指定类型的图片
                if (url.includes('Account-Header')) {
                    UGGBrowser = browser
                    resolve()
                }
                if (url.startsWith('https://dd.prod.captcha-delivery.com/image/') && (url.endsWith('.png') || url.endsWith('.jpg'))) {
                    console.log(`Intercepted response: ${url}`);
                    imageCount += 1;
                    images.push(url);
                    if(images.length == 2) {
                        UGGBrowser = browser
                        resolve()
                    }
                }
            });

            // 导航到指定页面
            try {
                await page.goto(url, { timeout: 30000, waitUntil: 'load' });
                browser.disconnect()
                resolve();  // 成功时返回拦截到的图片和计数
            } catch (error) {
                // console.error('Page navigation failed:', error);
                reject(error); 
            }

        } catch (error) {
            console.error('Error during browser interaction:', error);
            reject(error);  // 捕获其他意外错误
        }
    });
}

// 生成一个随机的抖动值
const getRandomInt = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;

// 贝塞尔曲线模拟加速—匀速—减速的滑动
function generateTrajectory(startX, startY, endX, endY, steps) {
    const trajectory = [];
    const totalDistanceX = endX - startX;
    const totalDistanceY = endY - startY;

    let prevX = startX;
    let prevY = startY;

    // 模拟加速—匀速—减速
    for (let i = 0; i <= steps; i++) {
        // 使用贝塞尔曲线或加速曲线的比例
        const t = i / steps;

        // 贝塞尔曲线的加速和减速效果
        const easeOutQuad = t * (2 - t); // 简单的加速—减速曲线

        // 计算新的X和Y位置
        const newX = startX + easeOutQuad * totalDistanceX + getRandomInt(-2, 2); // 加入随机抖动
        const newY = startY + easeOutQuad * totalDistanceY + getRandomInt(-2, 2); // 加入随机抖动

        trajectory.push({ x: newX, y: newY });

        prevX = newX;
        prevY = newY;
    }

    return trajectory;
}

const cache = {};

async function downloadImage(url, filename) {
    const writer = fs.createWriteStream(filename);
    
    const response = await axios({
        url,
        method: 'GET',
        responseType: 'stream'
    });

    // 将下载的图片流写入文件
    response.data.pipe(writer);

    // 返回一个 Promise，等待文件写入完成
    return new Promise((resolve, reject) => {
        writer.on('finish', resolve);
        writer.on('error', reject);
    });
}

class BrowserScheduler {
    groupMap = {}
    browsers = []
    taskList = []
    currentTaskNumber = -1

    constructor(taskName) {
        this.init()
    }
    checkResultStatus(vendor, html) {
        if (vendor.includes('ugg')) {
            if (html.includes('403 Forbidden') || html.includes('429 Too Many Requests') ||
                html.includes('https://ct.captcha-delivery.com/c2.js') || !(html.includes('brand-menu'))
            ) 
            {
                return {
                    status: 403
                }
            }
        }
        if (vendor.includes('ralphlauren')) {
            if (html.includes('px-captcha-wrapper')) {
                return {
                    status: 403
                }
            }

        }
        return {
            status: 200
        }
    }
    // 获取所有的浏览器状态
    async init() {
        logger.info(`开始初始化浏览器调度>>>>`)
        const res1 = await this.sendMessageToAds('/api/v1/group/list?page=1&&page_size=100', 'get')
        if (res1.status == 200 && res1.data.code == 0) {
            const list = res1.data.data.list

            list.forEach(item => {
                this.groupMap[item.group_name] = item.group_id
            });
        }

        logger.info(`初始化分组成功 ${Object.keys(this.groupMap).length} 个分组读取成功`)

        const res = await this.sendMessageToAds('/api/v1/user/list?page=1&&page_size=100', 'get')
        if (res.status == 200 && res.data.code == 0) {
            const list = res.data.data.list
            list.forEach(item => {
                this.browsers.push({
                    groupName: item.group_name,
                    userId: item.user_id,
                    status: 'pendding',
                    lastTime: null,
                    error: 0
                })
                this.sendMessageToAds(`/api/v1/browser/stop?user_id=${item.user_id}`, 'get')
            });
            logger.info(`初始化浏览器成功 ${this.browsers.length} 个浏览器被读取成功`)
        } else {
            logger.error(`请求ads失败 code ${res}`)
            process.exit(1);
        }
    }
    taskListListener() {
        setInterval(async () => {
            let deleteIndex = this.browsers.findIndex(item => item.status == 'delete')
            if (deleteIndex > -1) {
                this.browsers.splice(deleteIndex, 1);
            }
            if (this.taskList.length > 0) {
                logger.info(`当前队列中的任务数量：${this.taskList.length}`);
                if (this.taskList.length > 0) {
                    const task = this.taskList.shift();
                    logger.info(`开始执行任务 ${task.url}`)
                    // 第一步查找已经存在的环境
                    let penddingBrowsers = null
                    const exitBrowsers = this.browsers.filter(item => {
                        let group_flag = item.groupName == task.vendor
                        if (group_flag && !penddingBrowsers && item.status == 'pendding') {
                            penddingBrowsers = item
                        }
                        return group_flag
                    })
                    const allBrowsers = this.browsers.filter(item => {
                        let group_flag = (item.groupName == task.vendor)
                        return group_flag
                    })
                    logger.info(`当前vendor ${task.vendor} 空闲的浏览器数量为 ${exitBrowsers.length} 存在的浏览器数量为 ${allBrowsers.length}`)
                    if (penddingBrowsers) {
                        logger.info(`任务 ${task.url} 匹配到浏览器 ${penddingBrowsers.userId}`)
                        penddingBrowsers.status = 'running'
                        penddingBrowsers.lastTime = new Date().getTime()
                        if (task.vendor == 'shein_de') {
                            this.executeSheinTask(task, penddingBrowsers)
                        } else if (task.vendor.includes('ralphlauren')) {
                            this.executeRalTask(task, penddingBrowsers)
                        } else if (task.vendor.includes('ugg')) {
                            this.executeUggTask(task, penddingBrowsers)
                        }
                        else if (task.vendor.includes('canadagoose')) {
                            this.executeCanadagooseTask(task, penddingBrowsers)
                        }
                    } else {
                        logger.warn(`任务 ${task.url} 未匹配到浏览器`)
                        let max = (task.vendor == 'shein_de')? 2 : maxBrowserScheduler
                        if (allBrowsers.length < max) {
                            let countrycode = task.vendor.split('_')[1]
                            if (countrycode == 'uk') {
                                countrycode = 'gb'
                            }
                            else if (countrycode == 'eu') {
                                countrycode = 'se'
                            }
                            else if (countrycode == 'gl') {
                                countrycode = 'mx'
                            }
                            else if (countrycode == 'uae') {
                                countrycode = 'ae'
                            }
                            let res
                            if (task.vendor.includes('ugg')) {
                                let body = {
                                    "name": task.vendor,
                                    "fingerprint_config": {
                                        random_ua: {"ua_browser":["firefox"],"ua_system_version":["Windows 10"]},
                                        browser_kernel_config: {"version": "ua_auto", "type":"firefox"}
                                    },
                                    // "user_proxy_config": {
                                    //     "proxy_soft": "other",
                                    //     "proxy_type": "http",
                                    //     "proxy_host": "p.webshare.io",
                                    //     "proxy_port": "80",
                                    //     "proxy_user": "iovufznd-rotate",
                                    //     "proxy_password": "hjcllsnibgoo"
                                    // },
                                    // "user_proxy_config": {
                                    //     "proxy_soft": "other",
                                    //     "proxy_type": "http",
                                    //     "proxy_host": "p.webshare.io",
                                    //     "proxy_port": "80",
                                    //     "proxy_user": "qyclsghe-US-rotate",
                                    //     "proxy_password": "2dyvqu4pblih"
                                    // },
                                    "proxyid": "random",
                                    // "user_proxy_config": {
                                    //     "proxy_soft": "no_proxy",
                                    // },
                                    "group_id": this.groupMap[task.vendor]
                                }
                                res = await this.sendMessageToAds('/api/v1/user/create', 'post', body)
                            } 
                            if (task.vendor.includes('ralphlauren')) {
                                
                                res = await this.sendMessageToAds('/api/v1/user/create', 'post', {
                                    "name": task.vendor,
                                    "fingerprint_config": {
                                        screen_resolution: stringArray[Math.floor(Math.random() * stringArray.length)],  
                                        browser_kernel_config: {"version": "ua_auto", "type":"chrome"},
                                        random_ua: {"ua_browser":["chrome"],"ua_system_version":["Mac OS X"]}
                                    },
                                    "proxyid": "random",
                                    "group_id": this.groupMap[task.vendor]
                                })
                            }
                            if (task.vendor.includes('canadagoose')) {
                                res = await this.sendMessageToAds('/api/v1/user/create', 'post', {
                                    "name": task.vendor,
                                    "fingerprint_config": {
                                        random_ua: {"ua_browser":["chrome"],"ua_system_version":["Windows 10"]}
                                    },
                                    "user_proxy_config": {
                                        "proxy_soft": "other",
                                        "proxy_type": "http",
                                        "proxy_host": "p.webshare.io",
                                        "proxy_port": "80",
                                        "proxy_user": "iovufznd-rotate",
                                        "proxy_password": "hjcllsnibgoo"
                                    },
                                    "group_id": this.groupMap[task.vendor]
                                })
                            }
                            if (task.vendor.includes('shein')) {
                                res = await this.sendMessageToAds('/api/v1/user/create', 'post', {
                                    "name": task.vendor,
                                    // "user_proxy_config": {
                                    //     "proxy_soft": "no_proxy",
                                    // },
                                    // "user_proxy_config": {
                                    //     "proxy_soft": "other",
                                    //     "proxy_type": "http",
                                    //     "proxy_host": "gw.dataimpulse.com",
                                    //     "proxy_port": "823",
                                    //     "proxy_user": "e1a3b77be4b8f8bcb967__cr.de",
                                    //     "proxy_password": "1f22fb9690ff2b38"
                                    // },
                                    "user_proxy_config": {
                                        "proxy_soft": "other",
                                        "proxy_type": "http",
                                        "proxy_host": "p.webshare.io",
                                        "proxy_port": "80",
                                        "proxy_user": "qyclsghe-DE-rotate",
                                        "proxy_password": "2dyvqu4pblih"
                                    },
                                    // "user_proxy_config": {
                                    //     "proxy_soft": "other",
                                    //     "proxy_type": "http",
                                    //     "proxy_host": "p.webshare.io",
                                    //     "proxy_port": "80",
                                    //     "proxy_user": "iovufznd-" + countrycode.toUpperCase() + "-rotate",
                                    //     "proxy_password": "hjcllsnibgoo"
                                    // },
                                    // "user_proxy_config": {
                                    //     "proxy_soft": "other",
                                    //     "proxy_type": "http",
                                    //     "proxy_host": "superproxy.zenrows.com",
                                    //     "proxy_port": "1337",
                                    //     "proxy_user": "DHCpx4tkPfGd",
                                    //     "proxy_password": "kukechen_country-de"
                                    // },
                                    "group_id": this.groupMap[task.vendor]
                                })
                            }
                            if (res.status == 200 && res.data.code == 0) {

                                logger.warn(`创建浏览器成功 ${task.vendor}`)
                                const ret = res.data.data
                                this.browsers.push({
                                    groupName: task.vendor,
                                    userId: ret.id,
                                    status: 'pendding',
                                    lastTime: null,
                                    error: 0
                                })
                                this.taskList.push(task)
                                this.currentTaskNumber--
                                logger.warn(`任务重新添加到任务列表成功！`)
                            } else {
                                allResults[task.url] = '500:no browsers'
                            }
                        } else {
                            if (task.waitCount) {
                                logger.warn(`任务 ${task.url} 重试次数为 ${task.waitCount}`)
                                task.waitCount++
                            } else {
                                logger.warn(`任务 ${task.url} 开始重试`)
                                task.waitCount = 1
                            }
                            if (!task.waitCount || task.waitCount < 2) {
                                this.currentTaskNumber--
                                logger.warn(`任务 ${task.url} 重新添加到等待列表`)
                                this.taskList.push(task)
                            } else {
                                logger.warn(`任务 ${task.url} 等待超时，设置500`)
                                allResults[task.url] = '500:no browsers'
                            }
                            // 否则直接超时
                        }
                    }
                }
            }
        }, 1000);
    }
    addTask(task = {
        vendor: '',
        url: '',
    }) {
        if (task.vendor && task.url) {
            this.taskList.push(task)
        }
    }
    async getResult(url, timeout = 60) {
        return new Promise((resolve, reject) => {
            let seconds = 0;
            // 每秒执行一次
            const intervalId = setInterval(() => {
                seconds += 1;
                if (allResults[url]) {
                    const data = allResults[url]
                    delete allResults[url]
                    resolve(data);
                } else {
                    // 当到达 30 秒时，返回结果并清除定时器
                    if (seconds === timeout) {
                        clearInterval(intervalId);
                        reject("获取结果超时");
                    }
                }
            }, 1000);
        });
    }

    doDeleteBrowser(penddingBrowsers) {
        this.sendMessageToAds(`/api/v1/browser/stop?user_id=${penddingBrowsers.userId}`, 'get').then((res) => {
            logger.info(`再次关闭浏览器成功:${penddingBrowsers.userId}`)
            setTimeout(() => {
                this.sendMessageToAds(`/api/v1/user/delete`, 'post', { user_ids: [penddingBrowsers.userId] }).then(res => {
                    if (res.data.code == 0) {
                        logger.info(`再次删除浏览器成功:${penddingBrowsers.userId}`)
                        if(penddingBrowsers.groupName.includes('ugg')) {
                            const res2 = this.sendMessageToAds('/api/v1/user/list?page=1&&page_size=100', 'get')
                            if (res2.status == 200 && res2.data.code == 0) {
                                const list = res2.data.data.list
                                list.forEach(item => {
                                    if(item.group_name.includes('ugg')) {
                                        this.sendMessageToAds(`/api/v1/browser/stop?user_id=${item.user_id}`, 'get')
                                    }
                                });
                            }
                        }
                    } else {
                        logger.error(`再次删除浏览器失败:${penddingBrowsers.userId}`)
                    }
                })
            }, 2000)
        })
    }

    deleteBrowser(penddingBrowsers) {
        
        this.sendMessageToAds(`/api/v1/browser/stop?user_id=${penddingBrowsers.userId}`, 'get').then((res) => {
            console.log(res.data)
            logger.info(`关闭浏览器成功:${penddingBrowsers.userId}`)
            if(penddingBrowsers.groupName.includes('ugg')) {
                const res2 = this.sendMessageToAds('/api/v1/user/list?page=1&&page_size=100', 'get')
                if (res2.status == 200 && res2.data.code == 0) {
                    const list = res2.data.data.list
                    list.forEach(item => {
                        if(item.group_name.includes('ugg')) {
                            this.sendMessageToAds(`/api/v1/browser/stop?user_id=${item.user_id}`, 'get')
                        }
                    });
                }
            }


            setTimeout(() => {
                this.sendMessageToAds(`/api/v1/user/delete`, 'post', { user_ids: [penddingBrowsers.userId] }).then(res => {
                    if (res.data.code == 0) {
                        logger.info(`删除浏览器成功:${penddingBrowsers.userId}`)




                    } else {
                        logger.error(`删除浏览器失败:${penddingBrowsers.userId}`)
                        this.doDeleteBrowser(penddingBrowsers)
                    }
                })
            }, 2000)
        })
    }

    stopBrowser(penddingBrowsers) {
        this.sendMessageToAds(`/api/v1/browser/stop?user_id=${penddingBrowsers.userId}`, 'get').then((res) => {
            logger.info(`关闭浏览器成功:${penddingBrowsers.userId}`)
            setTimeout(() => {
                this.sendMessageToAds(`/api/v1/user/update`, 'post', {
                    "user_id": penddingBrowsers.userId,
                    "open_urls": [],
                    "cookie": []
                }).then((res) => {
                    logger.info('------ 清理cookie成功 -----')
                    penddingBrowsers.status = 'pendding'
                })
            }, 2000)

        })
    }


    async executeSheinTask(task, penddingBrowsers) {
        const { url, vendor } = task
        const ids = url.split(',')
        const result = {}
        this.sendMessageToAds(`/api/v1/browser/start?user_id=${penddingBrowsers.userId}&&open_tabs=1&&headless=0`, 'get')
            .then((async res => {
                if (res.status == 200 && res.data.code == 0) {
                    logger.info(`浏览器启动成功 端口:${res.data.data.debug_port}`)
                    let puppeteerUrl = res.data.data.ws.puppeteer
                    const browser = await puppeteer.connect({
                        browserWSEndpoint: puppeteerUrl,
                        defaultViewport: null
                    });
                    // 获取所有已经打开的页面
                    const pages = await browser.pages();
                    // 使用第一个页面
                    const page = pages[0];
                    // 读取本地的 shein_2.js 文件内容

                    // 启用请求拦截
                    await page.setRequestInterception(true);

                    // 拦截特定的 JavaScript 文件并替换内容
                    page.on('request', (request) => {
                        const url = request.url();
                        
                        if (request.resourceType() === 'image') {
                            if (url.includes('images3_ps1')) {
                                request.continue(); // 继续请求，保持原图片
                            }else {
                                request.respond({
                                    status: 200,
                                    contentType: 'image/png', // 根据你返回的图片类型调整
                                    body: imageBuffer, // 这将返回本地图片的内容
                                });
                            }
                        } else {
                            if (url.endsWith('5d3a4681b420b51b.js')) {
                                console.log(`替换js成功: ${url}`);
                                // 替换为本地的 shein_2.js 文件内容，并添加 CORS 头
                                request.respond({
                                    status: 200,
                                    contentType: 'application/javascript',
                                    headers: {
                                        'Access-Control-Allow-Origin': '*',  // 允许跨域访问
                                        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                                        'Access-Control-Allow-Headers': 'Content-Type'
                                    },
                                    body: jsContent,  // 替换为自定义的 JS
                                });
                            }else {
                                const resourceType = request.resourceType();
                                // 允许其他资源正常加载
                                if (cacheableTypes.includes(resourceType)) {
                                    // 如果该资源已经在缓存中，直接返回缓存的响应
                                    if (cache[url]) {
                                        try {
                                            logger.info(cache[url])
                                            request.respond(cache[url]);
                                        } catch (error) {
                                            request.continue();
                                        }
    
                                    } else {
                                        // 如果没有缓存资源，继续请求并缓存它
                                        request.continue();
                                    }
                                } else {
                                    // 对于其他非缓存资源，继续请求
                                    request.continue();
                                }
                            }
                            
                        }
                    });

                    page.on('response', async (response) => {
                        const url = response.url();
                        const resourceType = response.request().resourceType();
                        const cacheableTypes = ['script', 'stylesheet', 'image', 'font'];

                        // 只缓存特定类型的资源
                        if (cacheableTypes.includes(resourceType)) {
                            try {
                                const buffer = await response.buffer();
                                const headers = response.headers()
                                for (const key in headers) {
                                    if (obj.hasOwnProperty(key)) {
                                        const value = obj[key];

                                        // 检查值是否为字符串，且是否包含双引号
                                        if (typeof value === 'string' && value.includes('"')) {
                                            console.log(`Deleting key: ${key} (value contains a double quote)`);
                                            delete obj[key]; // 删除该键
                                        }
                                    }
                                }
                                cache[url] = {
                                    status: response.status(),
                                    headers: headers,
                                    contentType: headers['content-type'],
                                    body: buffer
                                };
                            } catch (error) {
                            }
                        }
                    });

                    let links = ['https://de.shein.com/Men-Apparel-c-2026.html',
                        'https://de.shein.com/category/Women-Knitwear-sc-0081653271.html',
                        'https://de.shein.com/recommend/Plus-Size-Casual-Dresses-sc-100176456.html',
                        'https://de.shein.com/style/QSFW-Clearance-sc-0011850135.html',
                        'https://de.shein.com/Women-Sleepwear-c-2332.html',
                        'https://de.shein.com/Baby-Girls-Onesies-c-2822.html',
                        'https://de.shein.com/new/New-Arrivals-sc-0021043511.html',
                        'https://de.shein.com/hotsale/WOMEN-UNDERWEAR-SLEEPWEAR-top-sc-003143975.html'
                    ]
                    let randomLink = links[Math.floor(Math.random() * links.length)];
                    await page.goto(randomLink, {timeout: 90000});

                    // 等待所有带有 static-image full-width 类的 div 加载
                    // await page.waitForSelector('div.static-image.full-width');

                    // // 使用 $$eval 来查找页面中所有符合条件的 div 元素，并选择第二个 div 下的第三个 a 标签
                    // await page.evaluate(() => {
                    //     let elements = document.querySelectorAll('.j-vue-coupon-package-container.c-vue-coupon');
                    //     elements.forEach(element => element.remove());
                    //     elements = document.querySelectorAll('.sui-modal.sui-modal__dialog');
                    //     elements.forEach(element => element.remove());
                    //     document.body.style.overflow = "auto";
                    //     elements = document.querySelectorAll('[class*="_shein_privacy_agreement_"]');
                    //     // 遍历找到的元素并将其从 DOM 中删除
                    //     elements.forEach(element => {
                    //         element.remove();
                    //     });

                    // });
                    // await page.$$eval('div.static-image.full-width', (divs) => {
                    //     if (divs.length >= 2) {
                    //         const secondDiv = divs[1]; // 选择第二个 div （索引从 0 开始）
                    //         const links = secondDiv.querySelectorAll('a'); // 获取该 div 下的所有 a 标签
                    //         if (links.length >= 3) {
                                
                    //             links[2].click(); // 点击第三个 a 标签
                    //         }
                    //     }
                    // });
                    // // 可选：等待一段时间，观察页面的变化
                    await delay(12000);
                    let changeTitle = getRandomString(6);

                    await page.evaluate((newTitle) => {
                        document.title = newTitle;
                    }, changeTitle); // 把 changeTitle 作为参数传递进去
                    // const hasLogoIcon = await page.evaluate(() => {
                    //     const element = document.querySelector('a#header_logo_icon');
                    //     return element !== null; // 如果找到该元素，返回 true，否则返回 false
                    // });
                    // if (!hasLogoIcon) {
                    //     throw new Error('页面中不存在 id 为 header_logo_icon 的 <a> 标签')
                    // }
                    // await new Promise(resolve => setTimeout(resolve, 5000));

                    // // 滚动到页面底部

                    // for (let i = 0; i < 14; i++) {
                    //     await page.evaluate(() => {
                    //         window.scrollBy(0, Math.floor(Math.random() * (150 - 120 + 1)) + 120);
                    //     });
                    //     await delay(500);
                    // }
                    //   await page.waitForNetworkIdle({idleTime: 5000});  // 等待网络空闲
                    await page.waitForSelector('.product-card__add-btn.price-wrapper__addbag-btn');
                    // 点击第一个 class="product-card__add-btn price-wrapper__addbag-btn" 的按钮
                    // 获取元素的位置
                    // await new Promise(resolve => setTimeout(resolve, 3000));
                    // 等待选择器加载并获取所有匹配的元素
                    await page.evaluate(() => {
                        let elements = document.querySelectorAll('.j-vue-coupon-package-container.c-vue-coupon');
                        elements.forEach(element => element.remove());
                        elements = document.querySelectorAll('.sui-modal.sui-modal__dialog');
                        elements.forEach(element => element.remove());
                        document.body.style.overflow = "auto";
                        elements = document.querySelectorAll('[class*="_shein_privacy_agreement_"]');
                        // 遍历找到的元素并将其从 DOM 中删除
                        elements.forEach(element => {
                            element.remove();
                        });

                    });
                    const elements = await page.$$('.product-card__add-btn.price-wrapper__addbag-btn');
                    const button = elements[2];  // 第三个元素（索引 2）
                    const box = await button.boundingBox();

                    // 模拟鼠标移动到按钮位置并点击
                    await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
                    await page.mouse.down();  // 模拟鼠标按下
                    await page.mouse.up();    // 模拟鼠标抬起
                    // await page.click('.product-card__add-btn.price-wrapper__addbag-btn');
                    let dianxuan = true
                    try {
                        
                    
                        console.log('未找到弹出部分，开始尝试过验证')
                        // 等待 class 为 geetest_item_img 的元素加载
                        // try {
                        //     await page.waitForSelector('.geetest_item_img', {
                        //         visible: true,  // 等待元素变得可见
                        //         timeout: 3000  // 超时时间设置为 30 秒（默认为 30 秒）
                        //     });
                        //     // 使用 page.evaluate 获取 class 为 geetest_item_img 的 img 元素的 src 属性
                        //     const imageSrc = await page.evaluate(() => {
                        //         const imgElement = document.querySelector('.geetest_item_img');
                        //         return imgElement ? imgElement.src : null;
                        //     });

                        //     // 输出结果
                        //     console.log('Image src:', imageSrc);

                        //     // 下载图片
                        //     const filepath = path.join(__dirname, 'downloaded_image.png'); // 保存图片的路径
                        //     await downloadImage(imageSrc, filepath);

                        //     // 将图片转换为 Base64
                        //     const base64Image = imageToBase64(filepath);
                        //     console.log('Base64 Image:', base64Image);
                        // }catch(e) {
                        // 等待 class 为 pic_wrapper 的元素加载
                        await page.waitForSelector('.pic_wrapper', {
                            visible: true,
                            timeout: 7000
                        });

                        // 获取 class 为 pic_wrapper 的元素的 background-image 属性
                        const backgroundImageUrl = await page.evaluate(() => {
                            const element = document.querySelector('.pic_wrapper');
                            if (element) {
                                // 获取 background-image 样式值
                                const style = window.getComputedStyle(element);
                                const backgroundImage = style.getPropertyValue('background-image');

                                // 提取 URL，如果存在背景图片
                                const urlMatch = backgroundImage.match(/url\(["']?(.+?)["']?\)/);
                                return urlMatch ? urlMatch[1] : null;
                            }
                            return null;
                        });


                        // 输出获取到的背景图片 URL
                        console.log('Background Image URL:', backgroundImageUrl);
                        const filepath = path.join(__dirname, 'downloaded_image.png'); // 保存图片的路径
                        await downloadImage(backgroundImageUrl, filepath);

                        // 将图片转换为 Base64
                        const base64Image = imageToBase64(filepath);
                        console.log('Base64 Image:', base64Image);
                        let data = qs.stringify({
                            'image': base64Image,
                            'direction': 'bottom',
                            'token': 'C_nHOXLUmpBpjd3DwXKamLbKxx20tLRJBI10cdtPe8Q',
                            'type': '30332',
                            'click_num': '3'
                        });
                        let config = {
                            method: 'post',
                            url: 'http://api.jfbym.com/api/YmServer/customApi',
                            headers: {},
                            data: data
                        };
                        const ret = await axios(config)
                        if (ret.data.msg = '识别成功') {
                            let zuobiao = ret.data.data.data.split('|')
                            const rect = await page.evaluate(() => {
                                const element = document.querySelector('.pic_wrapper');
                                if (element) {
                                    const { x, y, width, height } = element.getBoundingClientRect();
                                    return { x, y, width, height };
                                }
                                return null;
                            });

                            if (rect) {
                                // 输出元素的矩形信息
                                
                                console.log('Element position and size:', rect);
                                let param = ''
                                for(let i=0; i < zuobiao.length; i ++) {
                                    let item = zuobiao[i].split(',')
                                    const clickX = rect.x + Number(item[0]);
                                    const clickY = rect.y + Number(item[1]);
                                    // 使用 Puppeteer's mouse.click() 模拟点击指定坐标
                                    param = param + Number.parseInt(clickX) + ',' + Number.parseInt(clickY + 86) + '|'
                                }
                                param = param + '442,732'

                                await runPy('python mouse_clicker.py "' + param +'" ' + '"' + changeTitle + '"');
                                await delay(5000)
                                // 计算点击的全页面坐标 (54, 227) 是相对于元素的位置
                            } else {
                                console.log('pic_wrapper element not found');
                            }
                        }

                    } catch (error) {
                        dianxuan = false
                        console.log('未出现验证');
                    }
                    try {
                        await page.waitForSelector('.quick-view__info', {
                            visible: true,  // 等待元素变得可见
                            timeout: 3000  // 超时时间设置为 30 秒（默认为 30 秒）
                        });
                    }catch(error) {
                        if(dianxuan) {
                            await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
                            await page.mouse.down();  // 模拟鼠标按下
                            await page.mouse.up();    // 模拟鼠标抬起
                            await page.waitForSelector('.quick-view__info', {
                                visible: true,  // 等待元素变得可见
                                timeout: 3000  // 超时时间设置为 30 秒（默认为 30 秒）
                            });
                        }
                    }
                    // 在页面上下文中执行自定义的 JavaScript
                    const chStatus = await page.evaluate(() => {
                        return window.ch_status; // 直接返回页面中定义的全局变量
                    });
                    if (chStatus != "注入成功") {
                        throw new Error('---注入失败---')
                    }
                    for (let i = 0; i < ids.length; i++) {
                        let id = ids[i]
                        await page.evaluate((id) => {
                            window.ch.currentGoodsId = id;
                            console.log(`Set window.ch.currentGoodsId to "${id}"`);
                        }, id);
                        await delay(1000);
                    }
                    const goodsMap = await page.evaluate(() => {
                        return window.goodsMap; // 直接返回页面中定义的全局变量
                    });
                    allResults[url] = JSON.stringify(goodsMap)
                    // 断开 Puppeteer 与浏览器的连接，但不关闭浏览器
                    await browser.disconnect();
                    const copy = JSON.parse(JSON.stringify(penddingBrowsers));
                    this.deleteBrowser(copy)
                    penddingBrowsers.status = 'delete'

                } else {
                    logger.error(`浏览器启动出现问题`)
                    console.error(res.data)
                    throw new Error('---浏览器启动出现问题---')
                }
            })).catch(e => {

                allResults[url] = '500:浏览器启动失败'
                const copy = JSON.parse(JSON.stringify(penddingBrowsers));
                this.deleteBrowser(copy)
                penddingBrowsers.status = 'delete'
                console.error(e)
                // console.error(e)
                // const copy = JSON.parse(JSON.stringify(penddingBrowsers));
                // if (penddingBrowsers.error < 5) {
                //     penddingBrowsers.status = 'stop'
                //     penddingBrowsers.error++
                //     logger.error(`重启浏览器，浏览器错误次数:${penddingBrowsers.error}`)
                //     this.stopBrowser(penddingBrowsers)
                // } else {
                //     this.deleteBrowser(copy)
                //     penddingBrowsers.status = 'delete'
                //     console.error(e)

                // }

            })
    }

    async executeRalTask(task, penddingBrowsers) {
        const { url, vendor } = task
        const ids = url.split(',')
        const result = {}
        this.sendMessageToAds(`/api/v1/browser/start?user_id=${penddingBrowsers.userId}&&open_tabs=1&&headless=0`, 'get')
            .then((async res => {
                if (res.status == 200 && res.data.code == 0) {
                    logger.info(`浏览器启动成功 端口:${res.data.data.debug_port}`)
                    let puppeteerUrl = res.data.data.ws.puppeteer
                    const browser = await puppeteer.connect({
                        browserWSEndpoint: puppeteerUrl,
                        defaultViewport: null
                    });
                    
                    // 获取所有已经打开的页面
                    const pages = await browser.pages();
                    // 使用第一个页面
                    const page = pages[0];

                    

                    await page.setRequestInterception(true);
                    // 拦截特定的 JavaScript 文件并替换内容
                    page.on('request', (request) => {
                        const url = request.url();
                        if (request.resourceType() === 'image') {
                            request.respond({
                                status: 200,
                                contentType: 'image/png', // 根据你返回的图片类型调整
                                body: imageBuffer, // 这将返回本地图片的内容
                            });
                        } else {
                            const resourceType = request.resourceType();
                            // 允许其他资源正常加载
                            if (cacheableTypes.includes(resourceType)) {
                                // 如果该资源已经在缓存中，直接返回缓存的响应
                                if (cache[url]) {
                                    try {
                                        logger.info(cache[url])
                                        request.respond(cache[url]);
                                    } catch (error) {
                                        request.continue();
                                    }

                                } else {
                                    // 如果没有缓存资源，继续请求并缓存它
                                    request.continue();
                                }
                            } else {
                                // 对于其他非缓存资源，继续请求
                                request.continue();
                            }
                        }
                    });
                    let setCookie = ''
                    page.on('response', async (response) => {
                        const url = response.url();
                        const resourceType = response.request().resourceType();
                        const cacheableTypes = ['script', 'stylesheet', 'image', 'font'];
                        // 检查 URL 是否包含 'Sites-RLEU_Sterling-Site'
                        if (url.includes('Header-MenuFlyouts')) {
                            console.log(`捕获到的 URL: ${url}`);

                            // 获取 'set-cookie' headers
                            let headers = response.headers()
                            setCookie = headers['set-cookie'];
                            
                            if (setCookie) {
                            console.log(`Set-Cookie 头部: ${setCookie}`);
                            } else {
                            console.log('该响应未包含 Set-Cookie 头部');
                            }
                        }
                        // 只缓存特定类型的资源
                        if (cacheableTypes.includes(resourceType)) {
                            try {
                                const buffer = await response.buffer();
                                const headers = response.headers()
                                for (const key in headers) {
                                    if (obj.hasOwnProperty(key)) {
                                        const value = obj[key];

                                        // 检查值是否为字符串，且是否包含双引号
                                        if (typeof value === 'string' && value.includes('"')) {
                                            console.log(`Deleting key: ${key} (value contains a double quote)`);
                                            delete obj[key]; // 删除该键
                                        }
                                    }
                                }
                                cache[url] = {
                                    status: response.status(),
                                    headers: headers,
                                    contentType: headers['content-type'],
                                    body: buffer
                                };
                            } catch (error) {
                            }
                        }

                    });

                    await page.goto(url, {timeout: 240000});
                    await delay(3000);
                    const pageTitle = await page.title();
                    // 判断标题是否为 'Access to this page has been denied'
                    if (pageTitle === 'Access to this page has been denied') {
                        console.log('Page access has been denied.');
                        // 出现验证
                        let changeTitle = getRandomString(6);

                        await page.evaluate((newTitle) => {
                            document.title = newTitle;
                        }, changeTitle);

                        const centerPoint = await page.evaluate(() => {
                            const element = document.getElementById('px-captcha');
                            if (element) {
                              const rect = element.getBoundingClientRect(); // 获取元素的边界框信息
                              return {
                                centerX: Math.round(rect.left + rect.width / 2),
                                centerY: Math.round(rect.top + rect.height / 2) - 5,
                              };
                            }
                            return null; // 如果元素不存在
                        });
                        
                        if (!centerPoint) {
                            throw new Error('---出现ral验证错误---')
                        }else {
                            console.log('centerPoint')
                            console.log(centerPoint)
                        }

                        let param = `${centerPoint.centerX}, ${centerPoint.centerY + 87}`
                        await runPy2('python mouse_clicker_ral.py "' + param +'" ' + '"' + changeTitle + '"');
                        await page.mouse.move(centerPoint.centerX, centerPoint.centerY)
                        await page.mouse.down()
                        await delay(4000);
                        await page.mouse.move(centerPoint.centerX, centerPoint.centerY)
                        await delay(3000);
                        await page.mouse.move(centerPoint.centerX, centerPoint.centerY)
                        await delay(3000);
                        await page.mouse.up()

                        // let param = '412,624'
                        // await runPy2('python mouse_clicker_ral.py "' + param +'" ' + '"' + changeTitle + '"');
                        // await page.mouse.move(412, 537)
                        // await page.mouse.down()
                        // await delay(4000);
                        // await page.mouse.move(411, 538)
                        // await delay(3000);
                        // await page.mouse.move(410, 536)
                        // await delay(3000);
                        // await page.mouse.up()
                        // await delay(3000);
                        await page.waitForSelector('a.logo-link', { timeout: 30000 });

                        // throw new Error('---出现ral验证---')
                    } else {
                        console.log('Page title is:', pageTitle);
                    }
                    // const urlParams = new URL(url).searchParams;

                    // 获取 scroll 参数的值
                    // const scrollValue = urlParams.get('scroll') || urlParams.get('scorll');
                    // if(scrollValue) {
                        
                    //     for (let i = 0; i < 15; i++) {
                    //         await page.evaluate(async () => {
                    //             await new Promise((resolve) => {
                    //                 const distance = 1000;
                    //                 const delay = 50;    // 每次滚动的延迟时间，以毫秒为单位
                    //                 const timer = setInterval(() => {
                    //                     window.scrollBy(0, distance);
                    //                     // 当滚动到页面底部时，停止滚动
                    //                     if (window.scrollY + window.innerHeight >= (document.body.scrollHeight - 500)) {
                    //                         clearInterval(timer);
                    //                         resolve();
                    //                     }
                    //                 }, delay);
                    //             });
                    //         });
                    //         const moreButton = await page.$('a.more-button.button.inverse');
                            
                    //         if (moreButton) {
                    //             await page.evaluate(() => {
                    //                 let elements = document.querySelectorAll('#onetrust-consent-sdk');
                    //                 elements.forEach(element => element.remove());
                    //                 elements = document.querySelectorAll('.bxc.bx-base.bx-custom.bx-active-step-1');
                    //                 elements.forEach(element => element.remove());
                    //             });
                    //             await page.evaluate((moreButton) => {
                    //                 moreButton.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    //             }, moreButton);
                    //             await delay(1000);
                    //             console.log("Found the 'more-button button inverse' <a> tag, clicking...");
                    //             await moreButton.click(); // 点击该按钮
                    //         } else {
                    //             console.log("The 'more-button button inverse' <a> tag was not found.");
                    //             break;
                    //         }
                    //         for (let i = 0; i < 3; i++) {
                    //             await delay(5000);
                    //             const loaderExists = await page.$('div.loader-indicator') !== null;
                    //             if (loaderExists) {
                    //                 console.log('Loader indicator is present on the page.');
                    //             } else {
                    //                 break;
                    //             }
                    //         }
                    //     }
                    // }
                    // const result = await page.content();
                    let result = setCookie
                    if(!result){
                        await page.waitForSelector('a.logo-link');
                        result = await page.evaluate(() => document.cookie);
                    }
                    await browser.disconnect();
                    logger.info(`设置${url}结果成功`)

                    const { status } = this.checkResultStatus(vendor, result)
                    if (status == 403) {
                        allResults[url] = '403:' + result
                    } else {
                        allResults[url] = result
                    }
                    if (status == 403) {
                        logger.info(`页面出现403开始删除浏览器`)
                        throw new Error('---浏览器启动出现问题403---')
                    } else {
                        penddingBrowsers.status = 'delete'
                        const copy = JSON.parse(JSON.stringify(penddingBrowsers));
                        this.deleteBrowser(copy)
                    }
                } else {
                    logger.error(`浏览器启动出现问题`)
                    console.error(res.data)
                    throw new Error('---浏览器启动出现问题---')
                }
            })).catch(e => {
                allResults[url] = '500:浏览器启动失败:' + e.toString()
                penddingBrowsers.status = 'delete'
                const copy = JSON.parse(JSON.stringify(penddingBrowsers));
                this.deleteBrowser(copy)
                console.error(e)
            })
    }

    

    executeUggTask(task, penddingBrowsers) {
        // 启动浏览器
        const { url, vendor } = task
        this.sendMessageToAds(`/api/v1/browser/start?user_id=${penddingBrowsers.userId}&&open_tabs=1&&headless=0`, 'get')
            .then((async res => {
                if (res.status == 200 && res.data.code == 0) {
                    let firefox_driver = res.data.data.webdriver
                    let port = res.data.data["marionette_port"]
                    let images = []
                    await startBrowserAndProcess(url, vendor, res, images)
                    if(images.length != 0) {
                        let jpgName = vendor + '_intercepted_image.jpg'
                        let pngName = vendor + '_intercepted_image.png'
                        for(let i = 0 ; i < images.length; i++) {
                            let item = images[i]
                            if(item.includes('jpg')) {
                                console.log('正在下载第一个图片...');
                                await downloadImage(item, jpgName);
                            }else {
                                // 同步下载第二个图片
                                console.log('正在下载第二个图片...');
                                await downloadImage(item, pngName);
                            }
                        }
                    }
                    await runPy('python ocr.py ' + vendor + ' ' + firefox_driver + ' '  + port + ' ' +  (images.length>0? 'start' : 'no'));
                    const result = fs.readFileSync('1.txt', 'utf-8');
                    fs.writeFileSync('1.txt', '', 'utf-8');
                    const { status } = this.checkResultStatus(vendor, result)
                    if (status == 403) {
                        allResults[url] = '403:' + result
                    } else {
                        allResults[url] = result
                        logger.info(`设置${url}结果成功`)
                    }
                    if (status == '403') {
                        UGGBrowser = null
                        logger.info(`页面出现403开始删除浏览器`)
                        const copy = JSON.parse(JSON.stringify(penddingBrowsers));
                        penddingBrowsers.status = 'delete'
                        this.deleteBrowser(copy)
                        // if (penddingBrowsers.error < 1) {
                        //     penddingBrowsers.status = 'stop'
                        //     penddingBrowsers.error++
                        //     this.stopBrowser(penddingBrowsers)
                        //     logger.error(`重启浏览器，浏览器错误次数:${penddingBrowsers.error}`)
                        // } else {
                        //     const copy = JSON.parse(JSON.stringify(penddingBrowsers));
                        //     penddingBrowsers.status = 'delete'
                        //     this.deleteBrowser(copy)
                        // }
                    } else {
                        penddingBrowsers.status = 'pendding'
                    }
                } else {
                    UGGBrowser = null
                    logger.error(`浏览器启动出现问题`)
                    console.error(res.data)
                    allResults[url] = '500:浏览器启动失败'
                    throw new Error('---浏览器启动出现问题---')
                }
            })).catch(e => {
                UGGBrowser = null
                allResults[url] = '500:浏览器启动失败'
                console.log(allResults[url])
                console.error(e)
                const copy = JSON.parse(JSON.stringify(penddingBrowsers));
                penddingBrowsers.status = 'delete'
                this.deleteBrowser(copy)
                // if (penddingBrowsers.error < 1) {
                //     penddingBrowsers.status = 'stop'
                //     penddingBrowsers.error++
                //     logger.error(`重启浏览器，浏览器错误次数:${penddingBrowsers.error}`)
                //     this.stopBrowser(penddingBrowsers)

                // } else {
                //     const copy = JSON.parse(JSON.stringify(penddingBrowsers));
                //     this.deleteBrowser(copy)
                //     penddingBrowsers.status = 'delete'
                //     console.error(e)
                //     logger.error(`浏览器启动失败`)
                // }
            })
    }

    async executeCanadagooseTask(task, penddingBrowsers) {
        const { url, vendor } = task
        this.sendMessageToAds(`/api/v1/browser/start?user_id=${penddingBrowsers.userId}&&open_tabs=1&&headless=0`, 'get')
            .then((async res => {
                if (res.status == 200 && res.data.code == 0) {
                    logger.info(`浏览器启动成功 端口:${res.data.data.debug_port}`)
                    let puppeteerUrl = res.data.data.ws.puppeteer
                    const browser = await puppeteer.connect({
                        browserWSEndpoint: puppeteerUrl,
                        defaultViewport: null
                    });
                    // puppeteer  获取当前页面下的 cookie akm_bmfp_b2 和 akm_bmfp_b2-ssn
                    // 获取所有已经打开的页面
                    // 获取所有当前页面的 cookies
                    let resultHeader = {}
                    const pages = await browser.pages();
                    // 使用第一个页面
                    const page = pages[0];
                    await page.setRequestInterception(true);
                    // 拦截特定的 JavaScript 文件并替换内容
                    page.on('request', (request) => {
                        const url = request.url();
                        if(!resultHeader['client_hints']) {
                            const headers = request.headers();
                            // 输出 sec-ch-ua
                            if (headers['sec-ch-ua']) {
                              resultHeader['client_hints'] = headers['sec-ch-ua']
                            }
                            // 输出 sec-ch-ua-platform
                            if (headers['sec-ch-ua-platform']) {
                              resultHeader['platform'] = headers['sec-ch-ua-platform']
                            }
                        }
                        
                        if (request.resourceType() === 'image') {
                            request.respond({
                                status: 200,
                                contentType: 'image/png', // 根据你返回的图片类型调整
                                body: imageBuffer, // 这将返回本地图片的内容
                            });
                        } else {
                            const resourceType = request.resourceType();
                            // 允许其他资源正常加载
                            if (cacheableTypes.includes(resourceType)) {
                                // 如果该资源已经在缓存中，直接返回缓存的响应
                                if (cache[url]) {
                                    try {
                                        logger.info(cache[url])
                                        request.respond(cache[url]);
                                    } catch (error) {
                                        request.continue();
                                    }

                                } else {
                                    // 如果没有缓存资源，继续请求并缓存它
                                    request.continue();
                                }
                            } else {
                                // 对于其他非缓存资源，继续请求
                                request.continue();
                            }
                        }
                    });

                    page.on('response', async (response) => {
                        const url = response.url();
                        const resourceType = response.request().resourceType();
                        const cacheableTypes = ['script', 'stylesheet', 'image', 'font'];

                        // 只缓存特定类型的资源
                        if (cacheableTypes.includes(resourceType)) {
                            try {
                                const buffer = await response.buffer();
                                const headers = response.headers()
                                for (const key in headers) {
                                    if (obj.hasOwnProperty(key)) {
                                        const value = obj[key];

                                        // 检查值是否为字符串，且是否包含双引号
                                        if (typeof value === 'string' && value.includes('"')) {
                                            console.log(`Deleting key: ${key} (value contains a double quote)`);
                                            delete obj[key]; // 删除该键
                                        }
                                    }
                                }
                                cache[url] = {
                                    status: response.status(),
                                    headers: headers,
                                    contentType: headers['content-type'],
                                    body: buffer
                                };
                            } catch (error) {
                            }
                        }
                    });

                    await page.goto(url, {timeout: 60000});
                    await page.waitForSelector('div#app', { timeout: 15000 });
                    const userAgent = await page.evaluate(() => navigator.userAgent);
                    console.log('User-Agent:', userAgent);
                    resultHeader['user_agent'] = userAgent
                    const cookies = await page.cookies();

                    // 过滤出你需要的 cookies
                    const akm_bmfp_b2 = cookies.find(cookie => cookie.name === 'akm_bmfp_b2');
                    const akm_bmfp_b2_ssn = cookies.find(cookie => cookie.name === 'akm_bmfp_b2-ssn');
                    await browser.disconnect();
                    logger.info(`设置${url}结果成功`)
                    const result = JSON.stringify({
                        cookies: [
                            akm_bmfp_b2,
                            akm_bmfp_b2_ssn
                        ], 
                        headers: resultHeader
                    })
                    const { status } = this.checkResultStatus(vendor, result)
                    if (status == 403) {
                        
                        allResults[url] = '403:' + result    
                    } else {
                        allResults[url] = result
                    }
                    if (status == 403) {
                        logger.info(`页面出现403开始删除浏览器`)
                        throw new Error('---浏览器启动出现问题403---')
                    } else {
                        penddingBrowsers.status = 'delete'
                        const copy = JSON.parse(JSON.stringify(penddingBrowsers));
                        this.deleteBrowser(copy)
                    }
                } else {
                    logger.error(`浏览器启动出现问题`)
                    console.error(res.data)
                    throw new Error('---浏览器启动出现问题---')
                }
            })).catch(e => {
                allResults[url] = '500:浏览器启动失败'
                penddingBrowsers.status = 'delete'
                const copy = JSON.parse(JSON.stringify(penddingBrowsers));
                this.deleteBrowser(copy)
                console.error(e)
            })
    }


    async sendMessageToAds(url, method, data) {
        if (isExecuting) {
            return new Promise((resolve, reject) => {
                // 如果有任务正在执行，将新任务放入队列
                queue.push({ url, method, data, resolve, reject });
            });
        }

        isExecuting = true;
        try {
            await delay(500); // 等待 500 毫秒（0.5秒）

            // 发送 HTTP 请求
            const result = await axios[method](adsHost + url, data);

            // 任务完成，设置 isExecuting 为 false
            isExecuting = false;

            // 如果队列中有更多任务，处理下一个任务
            if (queue.length > 0) {
                const nextRequest = queue.shift(); // 取出队列中的下一个任务
                this.sendMessageToAds(nextRequest.url, nextRequest.method, nextRequest.data)
                    .then(nextRequest.resolve)
                    .catch(nextRequest.reject); // 处理下一个任务
            }

            return result; // 返回请求结果
        } catch (error) {
            isExecuting = false;

            // 确认错误处理时也检查队列
            if (queue.length > 0) {
                const nextRequest = queue.shift(); // 继续处理队列中的任务
                this.sendMessageToAds(nextRequest.url, nextRequest.method, nextRequest.data)
                    .then(nextRequest.resolve)
                    .catch(nextRequest.reject);
            }

            throw error; // 抛出异常
        }
    }
}

const browserScheduler = new BrowserScheduler()
module.exports = browserScheduler