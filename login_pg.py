from flask import Flask,redirect,url_for,render_template,request,session,flash
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def APPEND(tfile,fline,sline,co,otf):

    f=open(tfile,"w")
    f1=fline
    f1+='\n'
    f.write(f1)
    f2=sline
    f2+='\n'
    f.write(f2)
    f3=co
    f3+='\n'
    f.write(f3)
    f4="####"+'\n'+otf
    f4+='\n'
    f.write(f4)
    f.close()

def SELECTED_DISPLAY_FN(LIST):
	g=[]
	lo=[]
	ll=[]
	st=[]
	ent=[]
	for i in LIST:
			g.append(i[0])
			lo.append(i[-5])
			h=i[1].split(";")
			jd=""
			for j in range(len(h)):
				if j==len(h)-1:
					jd+=h[j]+"."
				else:
					jd+=h[j]+","
			st.append(jd)
			t=i[-6].split(";")
			jd=""
			for j in range(len(t)):
				if j==len(t)-1:
					jd+=t[j]+"."
				else:
					jd+=t[j]+","
			ent.append(jd)
	
	s=len(g)
	return g,lo,s,st,ent 

app=Flask(__name__)
app.secret_key="hellofromtheotherside"

#displaying sign in page
@app.route("/")
def WELCOME():
	return render_template("welcomepage.html")











@app.route("/loginpagenew.html")
def login():
	return render_template("loginpagenew.html")
#getting info from signin page
@app.route("/submit",methods=["POST","GET"])
def GET_INFO_SIGNIN():
	if request.method=="POST":
		user=request.form["username"]
		password=request.form["password"]
		us=str(user)
		pw=str(password)
		session["user"]=us
		session["password"]=pw
		
		
		return redirect(url_for("CHECK"))
	else:
		return render_template("loginpagenew.html")

#displaying and getting information from the create an accoun page
@app.route("/create.html",methods=["POST","GET"])
def GET_INFO_CREATE():
	if request.method=="POST":
		user=request.form["username"]
		email=request.form["email"]
		clas=request.form["class"]
		password=request.form["password"]
		session["user"]=user
		session["class"]=clas
		session["email"]=email
		session["password"]=password
		return redirect(url_for("CREATE"))
	else:
		return render_template("create.html")		
#creating and storing info gotten from the create an account page and loging in to the home page
@app.route("/create")
def CREATE():
	f=open("login_data.csv","r")
	robj=csv.reader(f,delimiter=",")
	b=[]
	for a in robj:
		if any(a):
			b.append(a)
	f.close()
	f=open("login_data.csv","a")
	wobj=csv.writer(f,delimiter=",")
	u=session["user"]
	c=session["class"]
	e=session["email"]
	p=session["password"]
	for i in b:
		if "" in [u,e,c,p]:
			flash("All field data is mandatory")
			return redirect(url_for("GET_INFO_CREATE"))
		elif [u,e,c,p] == i:
			flash("Account already exists","error")
			return redirect(url_for("GET_INFO_CREATE"))
		elif u==i[0]:
			flash("Use a different user name","info")
			return redirect(url_for("GET_INFO_CREATE"))
		elif e==i[1]:
			flash("Account already exists with this email","info")
			return redirect(url_for("GET_INFO_CREATE"))
		elif c.isdigit()==False:
			flash("Enter a valid class","info")
			return redirect(url_for("GET_INFO_CREATE"))
	else:
		wobj.writerow([u,e,c,p])
		
		return redirect(url_for("HOMEPG"))
		
	f.close()
	







#cross checking the info gotten from the sign in page and loging in to the home page
@app.route("/check")
def CHECK():
	u=session["user"]
	p=session["password"]
	f=open("login_data.csv","r")
	robj=csv.reader(f,delimiter=",")
	b=[]
	for a in robj:
		if any(a):
			b.append(a)
	f.close()
	us=str(u)
	pw=str(p)
	
	for i in b:
		if us=="" or pw=="":
			flash("All field data are mandatory")
			return redirect(url_for("login"))
		elif us==i[0] and pw!=i[3]:
			flash("invalid password","info")
			return redirect(url_for("login"))
		elif us.lower()=="admin" and pw.lower()=="admin123":
			return render_template("homepg.html",username_1=session["user"],v="inherit")
		if us ==i[0] and pw==i[3]:
			return redirect(url_for("HOMEPG"))
			break
	else:
		flash("Account does not exist. Try again or create an account")
		return redirect(url_for("login"))

#displays the home page
@app.route("/homepg.html")
def HOMEPG():
	if session["user"].lower()!="admin":
		return render_template("homepg.html",username_1=session["user"],v="hidden")
	else:
		return render_template("homepg.html",username_1=session["user"],v="inherit")



#displays the college information about the given college(this is the pg where all the info abt a single college is found)
@app.route("/col_display")
def COL_DISPLAY():
	d=[]
	f1=open("collegeatt.csv","r")
	robj=csv.reader(f1,delimiter=",")
	for a in robj:
		if any(a):
			d.append(a)
	if "col" not in session:
		return redirect(url_for("HOMEPG"))
	else:
		ccheck=session["col"]

	b=[]
	l=[]
	l1=[]
	ch="third"
	for i in d:
		if i[0].lower()==ccheck.lower():
			fname=i[-1]
			logoc=i[-5]
			i1=i[-4]
			i2=i[-3]
			i3=i[-2]
			cname=i[0]
			session["fname"]=fname
			session["logoc"]=logoc
			session["i1"]=i1
			session["i2"]=i2
			session["i3"]=i3
			break
		if ccheck=="col_display":
			fname=session["fname"]
			logoc=session["logoc"]			
			i1=session["i1"]
			i2=session["i2"]
			i3=session["i3"]

	#else:
		#return "college not found"
	f=open(fname,"r")
	s=" "
	while s:
		s=f.readline()
		s=s.strip()
		b.append(s)
	for i in range(2,len(b)):
		if b[i]=="####":
			ch="fourth"
			continue
		if ch=="third":
			l.append(b[i])
		elif ch=="fourth":
			l1.append(b[i])
	if session["user"].lower()=="admin":
		
		return render_template("georgia.html",username_1=session["user"],first_half=b[0],second_half=b[1],third_half=l,fourth_half=l1,logo=logoc,img_1=i1,img_2=i2,img_3=i3,col_name=cname,v="inherit")

	else:
		return render_template("georgia.html",username_1=session["user"],first_half=b[0],second_half=b[1],third_half=l,fourth_half=l1,logo=logoc,img_1=i1,img_2=i2,img_3=i3,col_name=cname,v="hidden")
#getting information from the search bar of the home page and checking it
@app.route("/search_col",methods=["POST","GET"])
def SEARCH_COL():
	relatedsearch=[]
	if request.method=="POST":
		col=request.form["searchc"]
		if col=="":
			return redirect(url_for("HOMEPG"))
		if len(col)<=4:
			flash("More than four characters input required","info")
			return redirect(url_for("HOMEPG"))
		elif col.isalpha()==False:
			flash("Enter Valid Search")
			return redirect(url_for("HOMEPG"))
		session["col"]=col
		liststrip=["the","of","at","in",".",")","("]
	f=open("collegeatt.csv","r")
	robj=csv.reader(f,delimiter=",")
	b=[]
	for a in robj:
		if any(a):
			b.append(a)
	f.close()
	for i in b:
		g=i[0].upper()
		for j in liststrip:
			g=g.strip(j)
		if col.upper() in g.upper():
			relatedsearch.append(i[0])
	if relatedsearch==[]:
		flash("Unable to find the Exact Match. ","info")
		for i in b:
			if i[0][0].upper()==col[0].upper():
				relatedsearch.append(i[0])
	else:
		session["searched_col"]=relatedsearch
		return redirect(url_for("DISP_SEARCHED_COL"))

	if relatedsearch==[]:
		flash("No  Other Related Colleges Found")
	else:
		flash("Here are some Related Colleges:")
	session["searched_col"]=relatedsearch
	return redirect(url_for("DISP_SEARCHED_COL"))

		#if i[0].upper()==col.upper():
			#return redirect(url_for("COL_DISPLAY"))
	#else:
		#return "not found "

#intermediate displaying function
@app.route("/searched_col")
def DISP_SEARCHED_COL():
	d=[]
	g=[]
	lo=[]
	ll=[]
	st=[]
	ent=[]
	listsearched=[]
	if "searched_col" in session:
		searched_col=session["searched_col"]
		f1=open("collegeatt.csv","r")
		robj=csv.reader(f1,delimiter=",")
		for a in robj:
			if any(a):
				d.append(a)
		c=0
		for i in d:
			if c==len(searched_col):
				break
			if i[0].upper()==searched_col[c].upper():
				listsearched.append(i)
				c+=1
		for i in listsearched:
			g.append(i[0])
			lo.append(i[-5])
			h=i[1].split(";")
			jd=""
			for j in range(len(h)):
				if j==len(h)-1:
					jd+=h[j]+"."
				else:
					jd+=h[j]+","
			st.append(jd)
			t=i[-6].split(";")
			jd=""
			for j in range(len(t)):
				if j==len(t)-1:
					jd+=t[j]+"."
				else:
					jd+=t[j]+","
			ent.append(jd)
	
		s=len(g)
		if session["user"].lower()=="admin":
			return render_template("all_colleges.html",listn=g,listl=lo,username_1=session["user"],length=s,listst=st,listent=ent,v="inherit")
		else:
			return render_template("all_colleges.html",listn=g,listl=lo,username_1=session["user"],length=s,listst=st,listent=ent,v="hidden")
	






#displays all the colleges in the directory and prints them in a vague format
@app.route("/all_colleges.html")
def DISP_ALL_COLLEGES():
	d=[]
	g=[]
	lo=[]
	ll=[]
	st=[]
	ent=[]
	f1=open("collegeatt.csv","r")
	robj=csv.reader(f1,delimiter=",")
	for a in robj:
		if any(a):
			d.append(a)
	for i in d:
		g.append(i[0])
		lo.append(i[-5])
		h=i[1].split(";")
		jd=""
		for j in range(len(h)):
			if j==len(h)-1:
				jd+=h[j]+"."
			else:
				jd+=h[j]+","
		st.append(jd)
		t=i[-6].split(";")
		jd=""
		for j in range(len(t)):
			if j==len(t)-1:
				jd+=t[j]+"."
			else:
				jd+=t[j]+","
		ent.append(jd)
	
	s=len(g)
	if session["user"].lower()=="admin":
		return render_template("all_colleges.html",listn=g,listl=lo,username_1=session["user"],length=s,listst=st,listent=ent,v="inherit")
	else:
		return render_template("all_colleges.html",listn=g,listl=lo,username_1=session["user"],length=s,listst=st,listent=ent,v="hidden")


#gets the name of the college from the all colleges page(all_colleges) and directs it to the show college page(col_display)
@app.route("/<name>")
def CHECK_COL(name):
	d=[]
	session["col"]=name
	f1=open("collegeatt.csv","r")
	robj=csv.reader(f1,delimiter=",")
	for a in robj:
		if any(a):
			d.append(a)
	for i in d:
		if i[0].upper()==name.upper():
			return redirect(url_for("COL_DISPLAY"))
	if name=="col_display":
		return redirect(url_for("COL_DISPLAY"))
	#else:
		#return "not found 1"

#displays filter page
@app.route("/filter_search")
def filter_search():
	if session["user"].lower()=="admin":
		return render_template("Filter_search.html", username_1=session["user"],v="inherit")
	else:
		return render_template("Filter_search.html", username_1=session["user"],v="hidden")

#gets information from the filter page
@app.route("/check_filter",methods=["POST","GET"])
def INFO_GET_FILTERBY():
	if request.method=="POST":
		stream=request.form.get("stream")
		country=request.form.get("country")
		hostel=request.form.get("hostel")
		session["country"]=country
		session["stream"]=stream
		session["hostel"]=hostel

		return redirect(url_for("CHECK_FILTERBY"))

#filters out the colleges
@app.route("/check_filterby")
def CHECK_FILTERBY():
	d=[]
	g=[]
	lo=[]
	ll=[]
	st=[]
	ent=[]
	filter1=[]
	filter2=[]
	filter3=[]
	f1=open("collegeatt.csv","r")
	robj=csv.reader(f1,delimiter=",")
	for a in robj:
		if any(a):
			d.append(a)
	for i in d:
		if i[2].lower()==session["country"].lower():
			filter1.append(i)
	for i in filter1:
		spstream=i[1].split(";")
		for j in spstream:
			if j.upper()==session["stream"].upper():
				filter2.append(i)
	if filter2==[]:
		for i in filter1:
			g.append(i[0])
			lo.append(i[-5])
			h=i[1].split(";")
			jd=""
			for j in range(len(h)):
				if j==len(h)-1:
					jd+=h[j]+"."
				else:
					jd+=h[j]+","
			st.append(jd)
			t=i[-6].split(";")
			jd=""
			for j in range(len(t)):
				if j==len(t)-1:
					jd+=t[j]+"."
				else:
					jd+=t[j]+","
			ent.append(jd)
	
		s=len(g)
		if session["user"].lower()=="admin":
			return render_template("all_colleges.html",listn=g,listl=lo,username_1=session["user"],length=s,listst=st,listent=ent,v="inherit")
		else:
			return render_template("all_colleges.html",listn=g,listl=lo,username_1=session["user"],length=s,listst=st,listent=ent,v="hidden")

	for i in filter2:
		if session["hostel"].lower()=="yes":
			a="None"
		else:
			a=["Private","Shared"]
		sphostel=i[4].split(";")
		for j in sphostel:
			if j in a:
				filter3.append(i)
				break
			elif j.lower()==a.lower():
				filter3.append(i)
				break
	if filter3==[]:
		for i in filter2:
			g.append(i[0])
			lo.append(i[-5])
			h=i[1].split(";")
			jd=""
			for j in range(len(h)):
				if j==len(h)-1:
					jd+=h[j]+"."
				else:
					jd+=h[j]+","
			st.append(jd)
			t=i[-6].split(";")
			jd=""
			for j in range(len(t)):
				if j==len(t)-1:
					jd+=t[j]+"."
				else:
					jd+=t[j]+","
			ent.append(jd)
	
		s=len(g)
		if session["user"].lower()=="admin":
			return render_template("all_colleges.html",listn=g,listl=lo,username_1=session["user"],length=s,listst=st,listent=ent,v="inherit")
		else:
			return render_template("all_colleges.html",listn=g,listl=lo,username_1=session["user"],length=s,listst=st,listent=ent,v="hidden")


		

	else:
		for i in filter3:
			g.append(i[0])
			lo.append(i[-5])
			h=i[1].split(";")
			jd=""
			for j in range(len(h)):
				if j==len(h)-1:
					jd+=h[j]+"."
				else:
					jd+=h[j]+","
			st.append(jd)
			t=i[-6].split(";")
			jd=""
			for j in range(len(t)):
				if j==len(t)-1:
					jd+=t[j]+"."
				else:
					jd+=t[j]+","
			ent.append(jd)
	
		s=len(g)
		if session["user"].lower()=="admin":
			return render_template("all_colleges.html",listn=g,listl=lo,username_1=session["user"],length=s,listst=st,listent=ent,v="inherit")
		else:
			return render_template("all_colleges.html",listn=g,listl=lo,username_1=session["user"],length=s,listst=st,listent=ent,v="hidden")


		





#shows the questions of the aptitude

@app.route("/apt.html")	
def SHOW_APT():
	if session["user"].lower()=="admin":
		return render_template("apt1.html",username_1=session["user"],v="inherit")
	else:
		return render_template("apt1.html",username_1=session["user"],v="hidden")

@app.route("/aptq_1",methods=["POST","GET"])
#gets info from previous question and shows the current question
def APT_q_one():
	if request.method=="POST":
		stream=request.form.getlist("stream")
		session["stream"]=stream
		if session["user"].lower()=="admin":
			return render_template("apt2.html",username_1=session["user"],v="inherit")
		else:
			return render_template("apt2.html",username_1=session["user"],v="hidden")

	else:
		return redirect(url_for("SHOW_APT"))


@app.route("/aptq_2",methods=["POST","GET"])
def APT_q_two():
	if request.method=="POST":
		country=request.form.getlist("country")
		session["country"]=country
		if session["user"].lower()=="admin":
			return render_template("apt3.html",username_1=session["user"],v="inherit")
		else:
			return render_template("apt3.html",username_1=session["user"],v="hidden")
	else:
		return redirect(url_for("APT_q_one"))

@app.route("/aptq_3",methods=["POST","GET"])
def APT_q_three():
	if request.method=="POST":
		size=request.form.getlist("size")
		session["size"]=size
		if session["user"].lower()=="admin":
			return render_template("apt4.html",username_1=session["user"],v="inherit")
		else:
			return render_template("apt4.html",username_1=session["user"],v="hidden")
	else:
		return redirect(url_for("APT_q_two"))

@app.route("/aptq_4",methods=["POST","GET"])
def APT_q_four():
	if request.method=="POST":
		hostel=request.form.getlist("hostel")
		session["hostel"]=hostel
		if session["user"].lower()=="admin":
			return render_template("apt5.html",username_1=session["user"],v="inherit")
		else:
			return render_template("apt5.html",username_1=session["user"],v="hidden")
	else:
		return redirect(url_for("APT_q_three"))

@app.route("/aptq_5",methods=["POST","GET"])
def APT_q_five():
	if request.method=="POST":
		cmates=request.form.getlist("classmates")
		session["classmates"]=cmates
		if session["user"].lower()=="admin":
			return render_template("apt6.html",username_1=session["user"],v="inherit")
		else:
			return render_template("apt6.html",username_1=session["user"],v="hidden")
	else:
		return redirect(url_for("APT_q_four"))

#gets info from last question and directs it to apt_filter
@app.route("/aptq_6.html",methods=["POST","GET"])
def APT_q_six():
	if request.method=="POST":
		fee=request.form.getlist("fee")
		session["fee"]=fee
		return redirect(url_for("APT_FILTER"))
	else:
		return redirect(url_for("APT_q_five"))


#filters out the aptitude answers
@app.route("/apt_check")
def APT_FILTER():
	b=[]
	d=[]
	g=[]
	lo=[]
	ll=[]
	st=[]
	ent=[]
	
	cutdown_1=[]
	cutdown_2=[]
	cutdown_3=[]
	cutdown_4=[]
	cutdown_5=[]
	cutdown_6=[]
	stream=session["stream"]
	size=session["size"]
	classmates=session["classmates"]
	fee=session["fee"]
	hostel=session["hostel"]
	country=session["country"]


	f=open("collegeatt.csv","r")
	robj=csv.reader(f,delimiter=",")
	for a in robj:
		if any(a):
			b.append(a)
	for i in b:
		sstream=i[1].split(";")
		for j in range (0,len(sstream)):
			if sstream[j].lower() in stream:
				cutdown_1.append(i)
				break
	if cutdown_1==[]:
		return "cutdown_1 is empty"

	for i in cutdown_1:
				
		if i[2].capitalize() in session["country"]:
			
			if i in cutdown_2:
				pass
			else:
				cutdown_2.append(i)
				
			

	if cutdown_2==[]:
		
		g,lo,s,st,ent=SELECTED_DISPLAY_FN(cutdown_1)
		flash("Here are some Colleges you might like:","info")
		if session["user"].lower()=="admin":
			return render_template("all_colleges.html",listn=g,listl=lo,username_1=session["user"],length=s,listst=st,listent=ent,v="inherit")
		else:
			return render_template("all_colleges.html",listn=g,listl=lo,username_1=session["user"],length=s,listst=st,listent=ent,v="hidden")
	
	
	for i in cutdown_2:
		shostel=i[4].split(";")
		for j in range(0,len(shostel)):
			
			if shostel[j].capitalize() in hostel:
				
				if i in cutdown_3:
					pass
				else:
					cutdown_3.append(i)
				break

	if cutdown_3==[]:
		g,lo,s,st,ent=SELECTED_DISPLAY_FN(cutdown_2)
		flash("Here are some Colleges you might like:","info")
		if session["user"].lower()=="admin":
			return render_template("all_colleges.html",listn=g,listl=lo,username_1=session["user"],length=s,listst=st,listent=ent,v="inherit")
		else:
			return render_template("all_colleges.html",listn=g,listl=lo,username_1=session["user"],length=s,listst=st,listent=ent,v="hidden")
	
	
	
	for i in cutdown_3:

		sclassmates=i[5].split(";")
		for j in sclassmates:
			if j.lower() in classmates:
				if i in cutdown_4:
					pass
				else:
					cutdown_4.append(i)
				
				break
				
	if cutdown_4==[]:
		
			
		g,lo,s,st,ent=SELECTED_DISPLAY_FN(cutdown_3)
		flash("Here are some Colleges you might like:","info")
		if session["user"].lower()=="admin":
			return render_template("all_colleges.html",listn=g,listl=lo,username_1=session["user"],length=s,listst=st,listent=ent,v="inherit")
		else:
			return render_template("all_colleges.html",listn=g,listl=lo,username_1=session["user"],length=s,listst=st,listent=ent,v="hidden")
	

	for i in cutdown_4:
		sfees=i[-6].split(";")

		for j in sfees:

			if j.lower() in fee:
				if i in cutdown_5:
					pass
				else:
					cutdown_5.append(i)
				break
	if cutdown_5==[]:
		
		g,lo,s,st,ent=SELECTED_DISPLAY_FN(cutdown_4)
		flash("Here are some Colleges you might like:","info")
		if session["user"].lower()=="admin":
			return render_template("all_colleges.html",listn=g,listl=lo,username_1=session["user"],length=s,listst=st,listent=ent,v="inherit")
		else:
			return render_template("all_colleges.html",listn=g,listl=lo,username_1=session["user"],length=s,listst=st,listent=ent,v="hidden")
	
	
	
	for i in cutdown_5:

		if i[3].lower() in size:
			if i in cutdown_6:
				pass
			else:
				cutdown_6.append(i)
			

	if cutdown_6==[]:
		
	
		s=len(g)
		g,lo,s,st,ent=SELECTED_DISPLAY_FN(cutdown_5)
		flash("Here are some Colleges you might like(cutdown_5):","info")
		if session["user"].lower()=="admin":
			return render_template("all_colleges.html",listn=g,listl=lo,username_1=session["user"],length=s,listst=st,listent=ent,v="inherit")
		else:
			return render_template("all_colleges.html",listn=g,listl=lo,username_1=session["user"],length=s,listst=st,listent=ent,v="hidden")
	else:
		
		g,lo,s,st,ent=SELECTED_DISPLAY_FN(cutdown_6)
		flash("Here are some Colleges you might like(cutdown_6):","info")
		if session["user"].lower()=="admin":
			return render_template("all_colleges.html",listn=g,listl=lo,username_1=session["user"],length=s,listst=st,listent=ent,v="inherit")
		else:
			return render_template("all_colleges.html",listn=g,listl=lo,username_1=session["user"],length=s,listst=st,listent=ent,v="hidden")


@app.route("/help")
def help():
	if session["user"].lower()=="admin":
		return render_template("help.html",username_1=session["user"],v="inherit")
	else:
		return render_template("help.html",username_1=session["user"],v="hidden")



@app.route("/about")
def about():
	if session["user"].lower()=="admin":
		return render_template("aboutus.html",username_1=session["user"],v="inherit")
	else:
		return render_template("aboutus.html",username_1=session["user"],v="hidden")

#add a new college
@app.route("/admin_add",methods=["POST","GET"])
def admin_add():
	if request.method=="POST":
		col_name=request.form["col_name"]
		new_stream=request.form["new_stream"]
		new_country=request.form.get("new_country")
		new_size=request.form.get("new_size")
		new_hostel=request.form["new_hostel"]
		new_cmates=request.form.get("new_cmates")
		new_fee=request.form["new_fee"]
		fline=request.form["fline"]
		sline=request.form["sline"]
		co=request.form["co"]
		otf=request.form["otf"]
		f=open("collegeatt.csv","a")
		wobj=csv.writer(f,delimiter=",")
		n=col_name.split()
		if n[0].lower()=="the":
			comname=n[1].lower()
		else:
			comname=n[0].lower()
		img=[comname+'_logo.jpg',comname+'1.jpg',comname+'2.jpg',comname+'3.jpg']
		tfile=comname+'.txt'
		l=[col_name,new_stream,new_country,new_size,new_hostel,new_cmates,new_fee,img[0],img[1],img[2],img[3],tfile]
		wobj.writerow(l)
		f.close()
		APPEND(tfile,fline,sline,co,otf)
		f=open("updates.txt","a")
		a="College "+ col_name + " has been added"
		a+="\n"
		f.write(a)
		f.close()
		flash("College has been added")
		return  render_template("admin_add.html")
	else:
		return render_template("admin_add.html")


@app.route("/admin_update",methods=["POST","GET"])
def admin_update():
	b=[]
	if request.method=="POST":
		col_name=request.form["col_name"]
		new_stream=request.form["new_stream"]
		new_country=request.form.get("new_country")
		new_size=request.form.get("new_size")
		new_hostel=request.form["new_hostel"]
		new_cmates=request.form.get("new_cmates")
		new_fee=request.form["new_fee"]
		
		f=open("collegeatt.csv","r")
		robj=csv.reader(f,delimiter=",")
		for a in robj:
			if any(a):
				b.append(a)
		f.close()
		f=open("collegeatt.csv","w")
		wobj=csv.writer(f,delimiter=",")
		for i in b:
			if col_name.lower()==i[0].lower():
				i[1]=new_stream
				i[2]=new_country
				i[3]=new_size
				i[4]=new_hostel
				i[5]=new_cmates
				i[6]=new_fee
				wobj.writerow(i)
				f1=open("updates.txt","a")
				a="College "+ col_name + " has been updated"
				a+="\n"
				f1.write(a)
				f1.close()
				flash("College has been Updated")
			else:
				wobj.writerow(i)
		f.close()
		for i in b :
			if col_name.lower()==i[0].lower():
				break
		else:
			flash("College Not Found")
			return render_template("admin_update.html")

		
		return render_template("admin_update.html")


	else:
		return render_template("admin_update.html")


@app.route("/admin_delete",methods=["POST","GET"])
def admin_delete():
	b=[]
	if request.method=="POST":
		col_name=request.form["col_name"]
		f=open("collegeatt.csv","r")
		robj=csv.reader(f,delimiter=",")
		for a in robj:
			if any(a):
				b.append(a)
		f.close()
		f=open("collegeatt.csv","w")
		wobj=csv.writer(f,delimiter=",")
		for i in b:
			if col_name.lower()==i[0].lower():
				f1=open("updates.txt","a")
				a="College "+ col_name + " has been deleted"
				a+="\n"
			   
				f1.write(a)
				f1.close()
				flash("College has been Deleted")
			else:
				wobj.writerow(i)
		for i in b:
			if col_name.lower()==i[0].lower():
					
				break
		else:
			flash("College not Found")
			return render_template("admin_delete.html")
		return render_template("admin_delete.html")
	else:
		return render_template("admin_delete.html")


#displays all updated colleges
@app.route("/updates")
def updates():
	b=[]
	f1=open("updates.txt","r")
	s=" "
	while s:
		s=f1.readline()
		s=s.strip()
		b.append(s)
	f1.close()
	if session["user"].lower()=="admin":
		return render_template("updates.html",listu=b,username_1=session["user"],v="inherit")
	else:
		return render_template("updates.html",listu=b,username_1=session["user"],v="hidden")
    			




    	
        
    	
    	
#we can use @app.reoute("/<name>"") for the all colleges to get the name from the url and direct it to the required page by checking the href url given for each and
#using that information display a certain type of college.REMEMBER create the function with a variable parameter so u can check and correspond the values
#a url which has .html or a <a> tag can be linked to a non existing pg as long as the rreoute exists in python. it is not nessesary for the pg to have a .html string at the end
if __name__=="__main__": 
	app.run(debug=True)
