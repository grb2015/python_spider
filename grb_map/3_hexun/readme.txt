1. 首先运行hexun.py得到的是all_prince_commanpy_info.csv和all_prince_commanpy_profit.csv
2. 手动的将all_prince_commanpy_profit.csv的数据合并到all_prince_commanpy_info.csv得到all_province_commanpy_info_all_country_formated_addr.csv
3. 运行get_city.py，得到all_prince_commanpy_info_formataddr.txt。 将all_prince_commanpy_info_formataddr.txt合并到all_prince_commanpy_info.csv
4. 将all_province_commanpy_info_all_country_formated_addr.csv里面的利润等数值在excel中设置单元格格式，不使用逗号作为千分符(不然运行csv2json.py会报错)
5. 运行csv2json.py， 将csv转为json
6. 将得到的all_province_commanpy_info_all_country_formated_addr.json部署到IIS服务器上，前端直接读取Json即可

