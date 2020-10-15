import time

import hashlib

def md5(str):
    m = hashlib.md5()
    m.update(str.encode("utf-8"))
    return m.hexdigest()

def make_url(url):
    if ("origin.uu.netease.com" in url) or ("origin-lvlt.uu.netease.com" in url):
        sauth="1550546139_66aa6ec87f7524bf9e06696814b75c57"
        secret = "puknkRy59LCn7Ux3NARtG4FM6VGQvB"
        expire = str(int(time.time() + 86400 * 365))
        key_m = md5(sauth+expire+secret)
        key = "%s___%s_%s"%(sauth,expire,key_m)
        return "http://%s?sauth=%s"%(url,key)
  
    if "dl-rgame.uu.netease.com" in url:
        secret = "y4IT4E5aVAFEbpXaAce0n3xdRIxZHC"
        expire = str(int(time.time()+86400*365))
        uri = url.replace("dl-rgame.uu.netease.com","")

        #key_m = md5(uri + secret + expire)
        key_m = uri + secret + expire
        key_m1 = md5(key_m)
        return "http://%s?uu_expire=%s&uu_key=%s"%(url,expire,key_m1)


if __name__ == '__main__':
  # url="origin-lvlt.uu.netease.com/eamaster/s/shift/apex_legends/apex_legends/fg__ww_us_retail_binaries/apex_legendspcfg__ww_us_retail_binariesconcept_856__r5pc_r5staging_n458_cl506463_2020_04_15_06_34_pm1c01865b06bf4eb796febc265fc91961.zip"
  # url="origin.uu.netease.com/eamaster/s/shift/fifa/fifa_20_g4/patch__ww_x0_ww_empatch/fifa_20_g4pcpatch__ww_x0_ww_empatchconcept_121__cypresshills_retail_ww_4195611737b6d7b1f5f410c8d44e10499038a9f.zip"
  # print make_url(url)
    with open('url','r') as f_object:
        for url_list in f_object.readlines():
            #print ("\n"+make_url(url_list[:-1]))
            print("\n" + make_url(url_list))


