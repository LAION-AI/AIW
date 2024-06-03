# utils
import requests
import json

def parse_model_response(response: requests.Response):
    """
    Parse the response from the model server
    Args:
        response (requests.Response): The response from the model server
    Returns:
        dict: The parsed response as a dictionary
    """
    if response.status_code == 200:
        response_json = response.content.decode().split('\n\n')[-2].replace('data: ', '')
        return json.loads(response_json)
    else:
        return response.text
    
def get_temp_cookies():
    cookies = {
        'SERVERID': 'S0|Zhuhx',
        'cf_clearance': '2gcV8hnsG1SnJUgvRih5vI4nnt4emF_SQ81JcJiVEiM-1713086239-1.0.1.1-imWoUe6mxOHowJRo5m9UC6p7zC8S6KjMuJDs6.n3ggYl.Y1UO2WBzp0MovhEMbWrGaHbHjUJKHsUWUFsNDKQtw',
        '_ga_K6D24EE9ED': 'GS1.1.1713086242.1.1.1713086905.0.0.0',
        '_ga': 'GA1.1.1409861337.1713086242',
        '_ga_R1FN4KJKJH': 'GS1.1.1713086242.1.1.1713086905.0.0.0',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Sec-GPC': '1',
        'Connection': 'keep-alive',
        # 'Cookie': 'SERVERID=S0|Zhuhx; cf_clearance=2gcV8hnsG1SnJUgvRih5vI4nnt4emF_SQ81JcJiVEiM-1713086239-1.0.1.1-imWoUe6mxOHowJRo5m9UC6p7zC8S6KjMuJDs6.n3ggYl.Y1UO2WBzp0MovhEMbWrGaHbHjUJKHsUWUFsNDKQtw; _ga_K6D24EE9ED=GS1.1.1713086242.1.1.1713086905.0.0.0; _ga=GA1.1.1409861337.1713086242; _ga_R1FN4KJKJH=GS1.1.1713086242.1.1.1713086905.0.0.0',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }

    response = requests.get('https://chat.lmsys.org/', cookies=cookies, headers=headers)
    return response.cookies.get_dict()

def get_server_id(cookies):
    """
    Get the server ID from the chat.lmsys.org website
    Args:
        cookies (dict): The cookies for the chat.lmsys.org website
    Returns:
        str: The server ID

    """


    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,de;q=0.6',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        # 'cookie': '_gid=GA1.2.1912599086.1712936779; __cf_bm=E0vU7VFcren8ouhHuEU4P7QAhz7Fc2L6P8b4uJ8P3eo-1713154862-1.0.1.1-psxIYvN_FHac8Pqawa8a8gaAtCvO5ndIR8mPz5h6Ax4gvRL_xAeT.veHl6.6SCvoj0vfj7.zpSjkffJRBzEvpQ; cf_clearance=y1_9bYcCbZpNemHvMjfQzA2ceSj6yGH1JK29zjXfA_A-1713154916-1.0.1.1-uAsgu_5THCPuaDA.DqhlOjxqO7S6Z2AFgBGeAppd94qqyLUyVfEUdIPpDrTTqo.bsfXz82_EkGCc7vcBvKvfjA; _ga_K6D24EE9ED=GS1.1.1713154918.9.0.1713154918.0.0.0; SERVERID=S4|Zhyrb; _ga_R1FN4KJKJH=GS1.1.1713154923.9.0.1713154923.0.0.0; _ga=GA1.2.309799699.1712494683; _gat_gtag_UA_156449732_1=1',
        'origin': 'https://chat.lmsys.org',
        'referer': 'https://chat.lmsys.org/?__cf_chl_tk=IaCmZ.xXVhjL4Q50.Fk0fuCSf40U0FZsEmihnkyzm8k-1713154906-0.0.1.1-1471',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-full-version': '"123.0.6312.122"',
        'sec-ch-ua-full-version-list': '"Google Chrome";v="123.0.6312.122", "Not:A-Brand";v="8.0.0.0", "Chromium";v="123.0.6312.122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"15.0.0"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    }

    data = {
        'd89352d19bc94d151b3fc12b126da56561b79f8a1752c1553b0bda0a2ccf7122': 'c4.Sn1oEwOLKSQ_rId1IpmJDEFn492K_serjRQTP1jg-1713154906-1.1.1.1-jo2ubIa5Va0M5PJRyI9Kl48FHldJFCHuCVeBVDY7TDwqeE7c41CT1Mh6kE7nnfcH8H9OijQjkGyVziFA5dW4bsySjZcHnZkC_dqIMuMabjWxfY.sNYqKorl0H5feTtzS8VT2oM3rrfb8NBz.HUCVCNcBlyXhME6T0dZwdDW5tfIerhyiGVevqPj4Ri0Frq5pwgZUQ1jXpuCMlCcMo.DdDSYjVVGed6DHjVfPk2NFJ60Fh5Vlo_R.pqGKETagDhbxxJ4B6x.onZ_Zw4NcXW9ZEUEjRYXWtMqBBgBQVVClyFqmf0toggQXeqwv2rlI4Fdi8MqArAYbVerLzFoxF752BLKT_CVnFQ3mL9FboCy65F.CtwJhAIlVau_ADNK3P4FXFeJK.xr1zSg08ZN02X1_st0340Mor4IHTknsQkINcShV4Im1A3gT4iN3kzBmczfJUZbxR1TFPx8mQbA66CSCpnlcdlC6skohzgNaXh.60_nu2Hj6qsu8VnT2Ei0gw932Sw5S3Z1qFjFr8MDZgzEuBFq4ZuWvFHtjn2yE2NHjCE0wP7FJWjnG4fKtzho1VwBuVVpI888cIMwH6.iiZx5IPhxd4r1t0kQpDDX_ntVhfEAKLsZ9MYfd1.QtveUx5.AXTcfgTig9UvT2j19OHYMj4maVKHZqRDlhUwNHoAgWQ3hUqYsC0vhYie4qN3gYSYMjfy9mG5jWV8mMHVv_Zcyq_MuH8y4Gj5VhUzzhg3vyIGd4BsuwUIBr6M6oOmlkduv0EIYYxMbGkEgmxitgH6_rDP3kRAD_V34Beg1.L2X35g1o4D0mley8Yu3kgrxSVEi7ufr22YLZH04cocecgixN.nvjmW2smTi7S7kMyMzAAQrBgRVxDkG7EECuErgjp.krM1GCTLmfyCt25wqBmq8fUItb34vrMA1TFEUoa3kiJLXfLua841Y10ejvDd_DyxVaePNQatDT6q1fJ3ZZNczHFGRYD..9HiD_ZHZb_Khkvni9ZDS226Yqj0uh34TS2b0kUNXuPELen.rIvijKp.8N2o53tO031Ky63ARqCQ5adLT6wBnpPsQfdorRx7G7aMHMN_wrDwn01Hmv.eEhY6oXCo2KoxZtdtsy6QX6zqkTqhqFsK2ZMziLDxBFShwy5xmxfZXt6YHjcectkN.KrTThkQI9lHc7W0r4SzQA13O2OtC3ftzCayAvWKY3X5HEGIzx6EIaY6LvM6Yweze4Phz05c3PkBYv7eigKFIDvoOhS5cn_ACjQ.1L0fZXjA5dLb52p6iRIzj_r_ZbWuaJzsa7cAMn2EYPu6ZcnuJ07QZOrAsXxJPQhzbNkBxuj.BGfHe4A9SWp1TlhpeLmLEp9QTR9Gz1xiJClCPue7Q__h24FF6_LYg583sH_QtbNcjge_3u',
        '1dd9fe2a929de48cc2dbbab6ec0a6147b087866e3e77a91828f868bd7e8eb004': 'xVxdhGpINtnk4KX9kobgWXRtRbp8sz6y0bXqA43HzYQ-1713154906-1.1.1.1-LiKmMyjihyLzvHS3NkZIHoGCy0EEGLoMDtKXui3oeBjH4sjyUatV4nsE_rGtp0muymvyYKnfPPXoZX0NVXAzQ9rGHARSSEcT83EL3J6tuQzA1Xf5mCbw4lMVYjeB3ju1XB0flhPse6MvFoipqutuLq581C.7NL4HX9p2oaNr0ldumUrRRA0t9Sg0_xmEkC4AxWPAp2f2M.t9l8uzpUOQdCuhc4z4EFDcGeQrS4cl3T8UXeSG3odhPG2yr9l0LGvG.DwqlxX3IeZKErU_6xSaFWT8u8C6DA6l_MQl.YhOOTO093r96cfSOz_mM5eCvhabpTEGi9fkJT9BzuXt0rODCWpnAfh.c4k_663p7esloo8plhCZHTuqVHBGr1QuAFGte99eYqxMXQngBVBeEujoLI5QuBNykq6Wly7s0urUFj7bRKM6p4s1dNqMDRZ3GrjB5PWRDDRPFYa7r4NSY.oh0EJ1WXWPF7AT2vIPl_Jc_p_Gsroj9Yuh7wsNVdiMtamwC6stjsRV408jkcxTkPwjDI7taLUya.dGl8DBRsWjf4u2MAQjXkLYC27lx_d44j._x73sJBvk004qTSkQzTyDEYzXadi.IpPMSeTIMMwBkO5h0aOgDOD61pyNWbEULUxlcUlnMwxfTmdTi0.IViIk7WdYlIq6xUSQb1hN_oDusRr2VkN3MB4pPpf3kWwGxohwUIMmvaMwhLDsa2oyhZdGTLCUcUcsDxu7Bm_H0O94j78YcyTM_wFEVsAHseFu7IcQ81.8I_6eAf8qnzk8SR6GtTrwYBTOJhAHIfvJxU3yM66A1eMzsAZhSnZm7JOs0thXCsEcXwr8s63PYyxfU.kiFFdqI_ubg97Y6NXxFsSSl.I0vcb5hU08t8tqKau2rZMpSXBxqRJH7Q0YFT9uhO_S_QEKUY7JVKNgn.0crAk9HfO.rTWlSPLYfL67Zo2.2vUZoKHz1HvIfv5VdAWCxCA5i8JSysImtZbInequCO4a2jdH4LmzkzD7fpfAczj12tPyuDIhLZRtqqOOKzVK8Jc8C1mamn0rw9TJFc3s7h.IiMJFy99tfX3rwegGgLzoCtDhPcpYjUeQcbV6xIOisUceiFAkozr0Hm6hVV1EyWowgOTahMhPO469zPxutTULZdNTyccP8ZB5RkZHMGNXMRrG4YrxPDLdE3Fm.bTYXMJhOdhqdKhWeYOB_9ZKxRCLKzxcM5erNamHrHp3EoGegXCyyTPD3XX7_mwSs0o4XYjUZl.zmSJNM1.6OQ0m5PfgAmS2L7ePst.wNwGmLNZyRFQg6tVTryDxLDHAA.FbaJ7kNIxDck9mtFPY5gjQPNZJs_AeU3Z3hQUzlgzbB6VN8GGa6s7jHRZNiDscjHjme5UWpJLtn.LqEVlB006a5QP9kd1nK7VEuvZFbrGsBvfYvYbcErbtdG9lWBIGnj6RTdkQ_txRUQ.ZO2EcdJEYaK46USsd.X0NF5GjigOU_f4_0QFZZgS.RKGDt_BUDn3dPg5qh2.aQ14aV6YkhIrgJchS5gaSku7F9WMIfCt82Lin7lIx3iF2ceBSYy_5oWK65YxYrJnbeupvulWBPtmEapu439u.mjxRjfrNgEa3USKlDUXSyyhETzJhr.JT94uxp8oLMEV6XhvmhgBSQEoV5uo9tqxQpM1HMp6zh6s2k0y0i_xTwP8XBtDSUNayV7HM4K5getENH6AlmzV1ARmQlsCBOrW9pCET4W8PPcFucs_St7MXFkPFBpjJ5moTYL9WhjqZoxAz6wdKM0OIme2o2iluSqnyNqflUewy6TrngY4FQzW5hFpLcofdHFsjAHk01vaW4C3ItVBbV4XM_5Je9eO_b8KwGkF2_bmR2krtxcz1Kg998_fcfhFWZHxKnnCUSWq_qmIcF7ynSkOJPF6ggvSxasZ3qS5L0z5TIxBxYZ0wD6EZBfe8jYX4XBLvt19_xAq.r3tXx6XSf5jat0mR54H5eZIfNoRL3RqYa24koZMw9AmQWGOMWnmuXQzeyXTS75NXKMNRD3RF.Dbda_GrXZM6rPki2Qgf4hJgqzK9mvzU8XQBE6sdKv_4oq8C86J.ur1.MjONuwUhvf4tR.xobXW.9IJLUKhfQx.Dh30s24e0MkMdssbjDwmnJ4.6YivluhInh2wizvRhaBq1HTy.LzHsVKGu_Bn_554rKFuptKCad77EL8zFMu.uOoFF4qhhFa85rtgEIV1hYnOhf1FjPnU3Dl2U3GqdoFWCiHQY26oRHD3Js1WxRhP5TAmZcFO_ASpXBTDKKIrp0pr30YvSNTK5YF_1NXgAe5vUHb4JH.n.8cugil6KbYirGYjTPIpcmlXO_ByowzJWJgNlhc9J98ieONaWJl3HRDOsMaf0j_93y.vDfCr8ZS2L6QRXUgaOpLNdQACiEK6Q6ePR8c7El0At66T97.tCYq9GVbXyOvMuDg5T4BxooD9Wnj1TG95kD.85qmZNqgWy0JeLR_bTaFR8tOERrRmPJAIhXXvjSIitzFMjPICk9lBPLkKkK1BlyyCPxDl2PpA3vk8IFfBsWINLvlwEtwalj5.FGVaOqVvjEhuOPHDe9JMuCAk2cLqaZAVQLIZq2mvRQey6K6Pic1fWIXNyj.qfK2ke4rmlJ7UH6FHCsvONiu.jWFaPmhZqXjZBsVHjZvDAPvVOrx0GZiEHwHBZdxZFkarXiyefttMA1XSFsuqa9DC2mPz0gImv9VgtoXIUKkvG7H.78uNG2Hf6nE7jL.Ss2zCRwNHfJTOHwFXqRQ',
        'c850fedcca414e53542346297ef3f0c249be7fe8e1d20db6e528aaa8a9b6da92': '4b3dae5767d1d9e89d54b01caef006ee',
        '6d99133979c3f2cc67ef6a3927267cfe66b4298cbae83a6469867c4dc7b12eee': 'uVzrgJqQqsdP-1-8749269518111e10',
        '9346b9a207cdb782023ba01ddea761c14fb3783573cccf570ec4f78d0fa820fa': '1d32a76c33fdfdceb0422fe092cf434c|{"managed_clearance":"i"}',
    }

    response = requests.post(
        'https://chat.lmsys.org/', 
        cookies=cookies, 
        headers=headers, 
        data=data
        )

    print(response)
    resp_cookies = response.cookies.get_dict()
    resp_cookies.update({'__cf_bm': cookies['__cf_bm'], 'cf_clearance': cookies['cf_clearance']})
    return resp_cookies


def get_cookies(SERVERID, __cf_bm, cf_clearance):
    """
    Get the cookies for the chat.lmsys.org website
    Args:
        server_id (str): The server ID
    Returns:
        dict: The cookies
    """
    cookies = {
        '__cf_bm': __cf_bm,
        'cf_clearance': cf_clearance,
        'SERVERID': SERVERID,
        '_ga_K6D24EE9ED': 'GS1.1.1713077461.1.1.1713078779.0.0.0',
        '_ga': 'GA1.2.582472446.1713077461',
        '_ga_R1FN4KJKJH': 'GS1.1.1713077462.1.1.1713078779.0.0.0',
        '_gid': 'GA1.2.1421087633.1713077470',
    }
    return cookies