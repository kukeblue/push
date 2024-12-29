import httpx

# 代理服务器配置
proxies = {
    "http://": "http://127.0.0.1:33210",
    "https://": "http://127.0.0.1:33210"
}

# 创建一个支持 HTTP/2 的客户端，并配置代理
client = httpx.Client(http2=True, proxies=proxies)

# 模拟Chrome浏览器的一般请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'upgrade-insecure-requests': '1',
    'Cookie': 'dwac_6dc903b7fbd09744cb96134f3f=eGyA2DthbSBuRhb3LKjc5-ep8FRUP4YLpwk%3D|dw-only|||GBP|false|Europe%2FLondon|true; cqcid=abZvECNxvYLjYeSfDNUfQgTqri; cquid=||; sid=eGyA2DthbSBuRhb3LKjc5-ep8FRUP4YLpwk; dwanonymous_5352b0208a2c38dda443555e36061458=abZvECNxvYLjYeSfDNUfQgTqri; dwsid=Uj5oRG2afojiBSNF5zqMkM37GMgCxJWjK0q2CIkRBo_UKlEs7LyE2u8pauK7hptP3i7rZ9qdMt4w1iVXq8uj1A==; layer0_bucket=90; layer0_destination=production; layer0_eid=d20030ea-c381-4652-94bd-53a3b1429d04; __cq_dnt=0; dw_dnt=0; osano_consentmanager_uuid=30d11b6f-93e6-4117-bc2a-a49add2f6e17; osano_consentmanager=ycdgvgR8pAWIqbiZ7G9jUpzTzoz8aYktLtOR_IDmHHmq7F2PqIFlkxfK3djYtTyknYz5EiWxL0gS6kuQfQLSEzKAQ2Kx7H2r4jHDuuSrGDvy0oHMPHG-695AwsNze2uWzDXgr6BcdIaO2uf6JYgt-ErZmo35tFfFNfn1OMyu7B0DjrW4aVR7aw9pT4CsBgwVT1lS72MwqzkFOaJjGtF0mIpsoOID7_kPVGSVU8S6cTXE_XooXbV0eWQbuQrNlBz5ioHy2t_2WomJthzDWX7sOc7gL3oJCMqi2yE0gw==; _dy_csc_ses=t; _dy_c_exps=; _dycnst=dg; _yob=chrome; _yobv=124; _dyid=4526117863445019425; _dyjsession=0bcaa286afad98e38d04e916217f739d; dy_fs_page=www.ugg.com%2Fuk%2Fwomen-clothing; _dycst=dk.w.c.ws.fst.; _dy_cs_gcg=Dynamic%20Yield%20Experiences; _dy_cs_cookie_items=_dy_cs_gcg; locale_pref=en_GB; _dyid_server=4526117863445019425; __pr.1oy9=medDbJizsc; _gcl_au=1.1.575862628.1714469669; ftr_ncd=6; ftr_blst_1h=1714469669551; __cq_uuid=abZvECNxvYLjYeSfDNUfQgTqri; __cq_seg=0~0.00!1~0.00!2~0.00!3~0.00!4~0.00!5~0.00!6~0.00!7~0.00!8~0.00!9~0.00; AMP_TOKEN=%24NOT_FOUND; _gid=GA1.2.827015231.1714469670; _scid=45e735a7-4253-474e-a775-925b5872afd2; _fbp=fb.1.1714469671757.1429998285; _tt_enable_cookie=1; _ttp=bDYXFEL-tGhdrB-a0oCJBMLnx_1; __attentive_id=cce47906b3394366837a5ce59581f502; _attn_=eyJ1Ijoie1wiY29cIjoxNzE0NDY5Njc0OTc2LFwidW9cIjoxNzE0NDY5Njc0OTc2LFwibWFcIjoyMTkwMCxcImluXCI6ZmFsc2UsXCJ2YWxcIjpcImNjZTQ3OTA2YjMzOTQzNjY4MzdhNWNlNTk1ODFmNTAyXCJ9In0=; __attentive_cco=1714469674983; _cs_c=0; mdLogger=false; kampyle_userid=ce15-e9d7-bef6-c5cd-7c0e-1ecf-7011-d55b; __attentive_dv=1; _sctr=1%7C1714406400000; _yop=n; _dy_c_att_exps=; _dy_geo=SG.AS.SG_.SG__Singapore; _dy_df_geo=Singapore..Singapore; kampyleUserSession=1714470909462; kampyleUserSessionsCount=5; _cs_mk_ga=0.9312796710601761_1714472376500; _yo=awvx1838vy959x1855y1080u; _dy_ses_load_seq=34308%3A1714472382638; visitCount=6; _dy_soct=561652.1084351.1714469667*764850.1453906.1714469667*780784.1479736.1714472382*884092.1832899.1714472382*491270.904151.1714472382*718163.1372655.1714472382*843261.1679943.1714472382*902234.1890364.1714472385; _dy_lu_ses=0bcaa286afad98e38d04e916217f739d%3A1714472387008; _dy_toffset=-3; utag_main=v_id:018f2e5b024400200b161f71c9680506f002606700bd0$_sn:1$_se:66$_ss:0$_st:1714474187737$ses_id:1714469667400%3Bexp-session$_pn:7%3Bexp-session$_prevpage:product%3Bexp-1714475987742$productlist:Men%3A%20Clothing%20%26%20Accessories%3A%20Coats%20%26%20Jackets%3Bexp-session$dc_visit:1$dc_event:8%3Bexp-session$dc_region:ap-east-1%3Bexp-session; _ga=GA1.2.924068313.1714469670; __cq_bc=%7B%22aaff-UGG-UK%22%3A%5B%7B%22id%22%3A%221152899%22%7D%5D%7D; _cs_id=eb4cc6da-4bd9-a893-d187-3d9b9c46bea9.1714469675.1.1714472391.1714469675.1.1748633675640.1; _cs_s=6.0.0.1714474191165; _uetsid=d873d50006d411ef9e072546872a4c6a; _uetvid=d874378006d411ef9889bb5715743856; _scid_r=45e735a7-4253-474e-a775-925b5872afd2; kampyleSessionPageCounter=2; forterToken=e6e76fb9e4bf42c6af4d005d3e16ccbf_1714472383581__UDF43-mnf-a4_6; __attentive_pv=5; __attentive_ss_referrer=https://www.ugg.com/uk/men-jackets-coats/?sz=11; datadome=uTcB7GJccuhRq6SVnVDE5Uas9tYaVmlAOvDqn3MpZFexUAKJQryYAcfbrZxt6W63fAX1p_X68pjXUYB0wElSmXTbc0mcFYaOugWEdW5HKyk6Y916FXPyvhmmngtTcCzv; _ga_84F0DJZGN6=GS1.1.1714469670.1.1.1714472420.16.0.0; _dd_s=rum=0&expire=1714473832356; pixlee_analytics_cookie_legacy=%7B%22CURRENT_PIXLEE_USER_ID%22%3A%2216571fbc-4a88-8a97-fb9c-463dc13164d2%22%2C%22TIME_SPENT%22%3A192%2C%22BOUNCED%22%3Afalse%7D',
    'dnt': '1'  # Do Not Track request header
}

# 发送请求
response = client.get('https://www.ugg.com/uk/janiya-bomber-jacket/1152899.html?dwvar_1152899_color=NAVY', headers=headers)

# 输出响应
print('HTTP version:', response.http_version)  # 确认使用的是HTTP/2
print('Status code:', response.status_code)
print('Response body:', response.text)

# 关闭客户端
client.close()