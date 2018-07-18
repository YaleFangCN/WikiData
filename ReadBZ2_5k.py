import json
import sys
from bz2 import BZ2File
import string
import pymysql

try:
    os.reload(sys)
    sys.setdefaultencoding("utf-8")
except:
    pass

conn = pymysql.connect(host="localhost", port=3306, user="root", passwd="root", db="wikidata1w", charset="utf8")
cur = conn.cursor()


def main():
    file_path = r"E:\WikiData\latest-all.json.bz2"

    Get_Json(file_path)
    cur.close()
    conn.close()

# entities表的插入操作：
def insert_entities(i, t):
    try:
        print("------------------------------------------------")
        sql_insert_entities = 'insert into web_main(entity_id,type,data_type,len,lable,description,aliase,site,title,badges)values(%(entity_id)s,%(type)s,%(data_type)s,%(len)s,%(label)s,%(description)s,%(aliase)s,%(site)s,%(title)s,%(badges)s)'
        params = {'entity_id': t['id'],
                  'type': t['type'],
                  'data_type': t['datatype'] if t['type'] == 'property' else None,
                  'len': 'en',
                  'label': t['labels']['en']['value'] if 'en' in t['labels'] else None,
                  'description': t['descriptions']['en']['value'] if 'en' in t['descriptions'] else None,
                  'aliase': json.dumps(t['aliases']['en']) if 'en' in t['aliases'] else None,
                  'site': t['sitelinks']['enwiki']['site'] if 'sitelinks' in t and 'enwiki' in t['sitelinks'] else None,
                  'title': t['sitelinks']['enwiki']['title'] if 'sitelinks' in t and 'enwiki' in t[
                      'sitelinks'] else None,
                  'badges': json.dumps(t['sitelinks']['enwiki']['badges']) if 'sitelinks' in t and 'enwiki' in t[
                      'sitelinks'] else None
                  }
        cur.execute(sql_insert_entities, params)
        conn.commit()
        print("第%s行的wikidata数据插入成功！！！" % i)
    except Exception as e:
        print(str(e))
        print("第%s行插入失败！！！" % i)


# claims表的插入操作：
def insert_claims(i, t):
    try:
        for key in t['claims']:
            Claim_arrays = t['claims'][key]
            for c in Claim_arrays:

                sql_insert_claims = 'insert into web_claims(id,entity_id,property_id,datavalue_value,datavalue_type,type,qualifiers_order,snaks_order,snaktype)values(%(id)s,%(entity_id)s,%(property_id)s,%(datavalue_value)s,%(datavalue_type)s,%(type)s,%(qualifiers_order)s,%(snaks_order)s,%(snaktype)s)'
                params = {'id': c['id'],
                          'entity_id': t['id'],
                          'property_id': c['mainsnak']['property'],
                          'datavalue_value': json.dumps(c['mainsnak']['datavalue']['value']) if 'datavalue' in c[
                              'mainsnak'] else None,
                          'datavalue_type': c['mainsnak']['datavalue']['type'] if 'datavalue' in c[
                              'mainsnak'] else None,
                          # 'datatype': c['mainsnak']['datatype'],
                          'type': c['type'],
                          # 'rank': c['rank'],
                          'qualifiers_order': c['qualifiers_order'] if 'qualifiers_order' in c else None,
                          'snaks_order': c['snaks_order'] if 'snaks_order' in c else None,
                          'snaktype': c['mainsnak']['snaktype']
                          }
                cur.execute(sql_insert_claims, params)
                conn.commit()
        print("第%s行的wikidata插入claims表成功" % i)
    except Exception as e:
        print(str(e))
        print("第%s行的wikidata插入claims表失败" % i)


# qualifiers表的插入操作：这里有三个主键，要注意！！！！
def insert_qualifiers(i, t):
    # error=''
    # error1=''
    try:
        for key in t['claims']:
            Claim_arrays = t['claims'][key]
            for c in Claim_arrays:
                if 'qualifiers' in c:
                    for qualifiers_key in c['qualifiers']:
                        Qualifiers_arrays = c['qualifiers'][qualifiers_key]
                        for q in Qualifiers_arrays:
                            #print(c['id'] + '---------------------')
                            sql_insert_qualifiers = 'insert into web_qualifiers(id,property_id,hash,snaktype,datavalue_value,datavalue_type,datatype)values(%(id)s,%(property_id)s,%(hash)s,%(snaktype)s,%(datavalue_value)s,%(datavalue_type)s,%(datatype)s)'
                            params = {'id': c['id'],
                                      'property_id': q['property'],
                                      'hash': q['hash'],
                                      'snaktype': q['snaktype'],
                                      'datavalue_value': json.dumps(
                                          q['datavalue']['value']) if 'datavalue' in q else None,
                                      'datavalue_type': q['datavalue']['type'] if 'datavalue' in q else None,
                                      'datatype': q['datatype']
                                      }
                            # error1=str(c['id'])

                            # error=str(q['property'])
                            cur.execute(sql_insert_qualifiers, params)
                            conn.commit()
        print("第%s行的wikidata插入qualifiers表成功" % i)
    except Exception as e:
        print(str(e))
        print("第%s行的wikidata插入qualifiers表失败" % i)
        # print(error1)


# reference表的插入操作：
def insert_reference(i, t):
    try:
        for key in t['claims']:
            Claim_arrays = t['claims'][key]
            for c in Claim_arrays:
                if 'references' in c:
                    for references_key in c['references']:
                        for snak_key in references_key['snaks']:
                            for r in references_key['snaks'][snak_key]:
                                sql_insert_references = 'insert into web_reference(id,property_id,snaktype,datavalue_value,datavalue_type,datatype)values(%(id)s,%(property_id)s,%(snaktype)s,%(datavalue_value)s,%(datavalue_type)s,%(datatype)s)'
                                params = {'id': c['id'],
                                          'property_id': r['property'],
                                          'snaktype': r['snaktype'],
                                          'datavalue_value': json.dumps(
                                              r['datavalue']['value']) if 'datavalue' in r else None,
                                          'datavalue_type': r['datavalue']['type'] if 'datavalue_type' in r else None,
                                          'datatype': r['datatype']

                                          }
                            cur.execute(sql_insert_references, params)
                            conn.commit()
        print("第%s行的wikidata插入references表成功" % i)

    except Exception as e:
        print(str(e))
        print("第%s行的wikidata插入references表失败" % i)


# 读取压缩文件json：
def ReadFile(file_path):
    try:
        f = BZ2File(file_path)
    except IOError:
        print("读取压缩json文件失败！！！")
        sys.int()
    return f
#
#
def Get_Json(file_path):
    i = 1
    count = 1
    f = ReadFile(file_path)
    for line in f:
        line_str = line.decode()
        print("第%s行长度是" % count + str(len(line_str)))
        '''用来断电记录存储到哪'''
        if count < 2:
            print("正在跳过第%s行" % count)
            count += 1
            continue
        if len(line_str) > 2:
            t = json.loads(line_str[0:-2])
            print(t)
            insert_entities(count, t)
            insert_claims(count, t)
            insert_qualifiers(count, t)
            insert_reference(count, t)
        else:
            print("第%s行不是wikidata数据!!" % count)

        i += 1
        count += 1
        # 插入到第count-1行停止，所以下次插入要从第count行开始，即要先跳过count-1行
        if count == 10001:
            break


if __name__ == '__main__':
    main()



