#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-05-22 15:20:05
# @Author  : zealous (doublezjia@163.com)
# @Link    : https://github.com/doublezjia
# @Version : $Id$
# @@Desc   : 获取企查查广东地区的企业信息

import os,requests,sys,csv,time,random
from bs4 import BeautifulSoup
from datetime import datetime

# 企查查广东地区的页面列表地址
base_url = 'https://www.qichacha.com/g_GD_{pagenum}.html'
# 企查查网站地址，用于补全获取的URL地址
head_url = 'https://www.qichacha.com'
# 请求头
headers = {
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0'
}

# cookies 通过登录网站可以获取 以字典形式保存
# cookies = {}

# csv的列表头
csv_List_head=('企业名称','曾用名','法定代表人','联系电话','邮箱地址','官方网站','企业地址',
	'所属行业','公司类型','经营状态','经营方式','人员规模','所属地区','营业期限','经营范围',
	'注册资本','实缴资本','成立日期','核准日期','登记机关','统一社会信用代码','纳税人识别号','注册号','组织机构代码')


#保存数据到csv文件
def save_csv(msg):
	with open('qichacha_company.csv','a',newline='') as datacsv:
		csvwriter = csv.writer(datacsv,dialect=('excel'))
		csvwriter.writerow(msg)


# 获取页面内容
def contentPage(url):
	url = url
	# 获取完整的电话号码和邮箱地址，请在requets.get()中添加cookies=cookies
	req = requests.get(url,headers=headers)
	soup = BeautifulSoup(req.text,'html.parser')
	# 判断网站是否正常打开
	if req.status_code == 200 :
		# 获取公司名
		try:
			conpanyname = soup.find('div',{'class':'row title'}).h1.text.strip()
		except AttributeError:
			sys.exit('获取不了目标页面内容,爬虫自动退出,请检查目标页面是否正常打开或者自动跳转到首页')
		# 获取电话、邮箱、官网、公司地址信息
		row = soup.find('div',{'class':'content'}).find_all('div',{'class':'row'})
		for i in row:
			# 判断是否i.find('span',{'class':'cdes'})有内容
			if i.find('span',{'class':'cdes'}):
				# 判断获取的i.find('span',{'class':'cdes'})是否为电话
				if i.find('span',{'class':'cdes'}).text.strip() == '电话：':
					try:
						tel = i.find('span',{'class':'cvlu'}).span.text.strip()
					except AttributeError:
						tel = i.find('span',{'class':'cvlu'}).text.strip()
					# 获取官网
					if i.find('span',{'class':'cdes'}).find_parent().find_next_sibling().text.strip() == '官网：':
						try:
							web = i.find('span',{'class':'cdes'}).find_parent().find_next_sibling().find_next('span').a.find_next('a').text.strip()
						except AttributeError:
							web = i.find('span',{'class':'cdes'}).find_parent().find_next_sibling().find_next('span').text.strip()
				# 判断获取的i.find('span',{'class':'cdes'})是否为邮箱
				if i.find('span',{'class':'cdes'}).text.strip() == '邮箱：':
					try:
						email = i.find('span',{'class':'cvlu'}).text.strip()
					except AttributeError:
						email = '暂无'
					# 获取地址
					if i.find('span',{'class':'cdes'}).find_parent().find_next_sibling().text.strip() == '地址：':
						try:
							address = i.find('span',{'class':'cdes'}).find_parent().find_next_sibling().find_next('span').a.text.strip()				
						except AttributeError:
							address = i.find('span',{'class':'cdes'}).find_parent().find_next_sibling().find_next('span').text.strip()

		# 获取公司法人名称
		try:
			legal_person = soup.find('div',{'class':'boss-td'}).find('a',{'class':'bname'}).text.strip()
		except AttributeError:
			legal_person = soup.find('div',{'class':'boss-td'}).find('a',{'class':'bcom'}).text.strip()
		
		# 获取公司的注册相关信息，通过定位table获取
		tablemsg = soup.find('table',{'class':'ntable'}).find_next('table').find_all('tr')
		for tr in tablemsg:
			# 判断每个tr中第一个td内容获取相关内容，同一个td的其他内容通过find_next()定位
			if tr.td.text.strip() == '注册资本：':
				Registered_capital = tr.td.find_next('td').text.strip()
				Paid_capital = tr.td.find_next('td').find_next('td').find_next('td').text.strip()
			if tr.td.text.strip() == '经营状态：':
				Operating_state = tr.td.find_next('td').text.strip()
				Date_of_establishment = tr.td.find_next('td').find_next('td').find_next('td').text.strip()
			if tr.td.text.strip() == '统一社会信用代码：':
				Usc_code = tr.td.find_next('td').text.strip()
				Tid_number = tr.td.find_next('td').find_next('td').find_next('td').text.strip()
			if tr.td.text.strip() == '注册号：':
				Registration_number = tr.td.find_next('td').text.strip()
				Organization_Code = tr.td.find_next('td').find_next('td').find_next('td').text.strip()
			if tr.td.text.strip() == '公司类型：':
				Type_of_company = tr.td.find_next('td').text.strip()
				Industry = tr.td.find_next('td').find_next('td').find_next('td').text.strip()
			if tr.td.text.strip() == '核准日期：':
				Date_of_approval = tr.td.find_next('td').text.strip()
				Registration_authority = tr.td.find_next('td').find_next('td').find_next('td').text.strip()
			if tr.td.text.strip() == '所属地区：':
				Area = tr.td.find_next('td').text.strip()
			if tr.td.text.strip() == '曾用名':
				Name_used_before = tr.td.find_next('td').text.strip()
				Operation_mode = tr.td.find_next('td').find_next('td').find_next('td').text.strip()
			if tr.td.text.strip() == '人员规模':
				Personnel_scale = tr.td.find_next('td').text.strip()
				Time_limit_for_business = tr.td.find_next('td').find_next('td').find_next('td').text.strip()
			if tr.td.text.strip() == '经营范围：':
				Scope_of_operation = tr.td.find_next('td').text.strip()

		print ('企业名称: %s' % conpanyname)
		print ('曾用名: %s ' % Name_used_before)
		print ('法定代表人: %s' % legal_person)
		print ('联系电话: %s' % tel)
		print ('邮箱地址: %s' % email)
		print ('官方网站: %s' % web)
		print ('企业地址: %s' % address)

		print ('所属行业: %s ' % Industry)
		print ('公司类型: %s ' % Type_of_company)
		print ('经营状态: %s ' % Operating_state)
		print ('经营方式: %s ' % Operation_mode)
		print ('人员规模: %s ' % Personnel_scale)
		print ('所属地区: %s ' % Area)
		print ('营业期限: %s ' % Time_limit_for_business)
		print ('经营范围: %s ' % Scope_of_operation)

		print ('注册资本: %s' % Registered_capital)
		print ('实缴资本: %s ' % Paid_capital)
		print ('成立日期: %s ' % Date_of_establishment)
		print ('核准日期: %s ' % Date_of_approval)
		print ('登记机关: %s ' % Registration_authority)
		print ('统一社会信用代码: %s ' % Usc_code)
		print ('纳税人识别号: %s ' % Tid_number)
		print ('注册号: %s ' % Registration_number)
		print ('组织机构代码: %s ' % Organization_Code)
		print ('\n')

		# 获取的企业信息
		Usc_code = "'" + Usc_code
		Tid_number = "'" + Tid_number
		Registration_number = "'" + Registration_number

		conpany_msg = (conpanyname,Name_used_before,legal_person,tel,email,web,
			address,Industry,Type_of_company,Operating_state,Operation_mode,
			Personnel_scale,Area,Time_limit_for_business,Scope_of_operation,
			Registered_capital,Paid_capital,Date_of_establishment,Date_of_approval,
			Registration_authority,Usc_code,Tid_number,
			Registration_number,Organization_Code)
		# 保存数据到csv文件
		save_csv(conpany_msg)
	else:
		sys.exit('网站打开异常，爬虫自动退出.')


# 主函数，获取企查查中显示的企业页面地址
def main():
	for num in range(1,3):
		url = base_url.format(pagenum=num)
		req  = requests.get(url,headers=headers)
		# 判断网站是否正常打开
		if req.status_code == 200 :
			soup = BeautifulSoup(req.text,'html.parser')
			data = soup.find_all(class_='panel-default')
			for item in data:
				# 获取每个页面的地址，然后发送到contentPage中处理
				conpany_url =head_url+item.find('a',{'class':'list-group-item clearfix'})['href']
				print ('企查查页面地址:%s' % conpany_url)

				contentPage(conpany_url)
					
				tnum = random.randint(2,8)
				print ('防止网站禁止爬虫，等待%s秒' % tnum)
				time.sleep(tnum)
		else:
			sys.exit('网站打开异常，爬虫自动退出.')


if __name__ == '__main__':
	# 获取爬虫开始时间
	start_time = datetime.now()
	print ('获取企查查广东地区的企业信息')
	print ('爬虫开始')
	# csv文件表格的列表头
	with open('qichacha_company.csv','w',newline='') as datacsv:
		csvwriter = csv.writer(datacsv,dialect=('excel'))
		csvwriter.writerow(csv_List_head)
	main()
	# 获取爬虫结束时间
	end_time = datetime.now()
	# 获取爬虫花费的时间
	use_time = end_time - start_time
	print ('爬虫结束,耗时%s，数据保存在qichacha_company.csv中' % use_time)

