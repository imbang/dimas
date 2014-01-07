import os
import cherrypy as cp 
import MySQLdb 
from jinja2 import Environment, FileSystemLoader
import atexit
import time
 

_curdir = os.path.join(os.getcwd(), os.path.dirname(__file__)) 
env = Environment(loader=FileSystemLoader('C:/cherrypy'))  
cp.config.update({'environment': 'embedded'}) 

if cp.__version__.startswith('3.0') and cp.engine.state==0:
    cp.engine.start(blocking=False)  
    atexit.register(cp.engine.stop) 
		   
def connect(thread_index): 
    # Create a connection and store it in the current thread 
    cp.thread_data.db = MySQLdb.connect('localhost', 'yyyyy', 'xxxxx', 'dimasdb') 
 
# Tell cp to call "connect" for each thread, when it starts up 
cp.engine.subscribe('start_thread', connect)

 
class Root: 
    def index(self):
		c = cp.thread_data.db.cursor()
		sql="select a.req_type,a.req_date,b.username,c.name,d.ele_name,a.path,e.proc_name,a.req_id from \
		datarequest a, dimas_user b , stations c, elements d, processor e\
		where a.processor_id=e.processor_id and a.elemen_id=d.ele_id and \
  a.sta_id=c.sta_id and a.user_id=b.id and req_type in(1,2) and status_id=0 \
		order by req_date ASC"
		c.execute(sql)
		res = c.fetchall()
		c.close()
		tmpl = env.get_template('index.html')
		return tmpl.render(data=res)
    index.exposed = True
    
    def MWFklim(self,serid,eleid,ele,staid,parid,permid,infile,outfile):
        i = 1
        if (ele in ['tg','tx','tn','pp']):
            multiplier = 10.
        else:
            multiplier = 1.
        
        try:
            fout = open(outfile,'w')
            sql = "insert into series values(%s,%s,%s,%s,%d);\n" % (serid,\
            eleid,staid,parid,permid)
            fout.write(sql)
            with open(infile,'r') as ifile:
                for line in ifile:
                    dt = line.strip().split()
                    tseries = dt[0]
                    if (i==1):
                        sdate = tseries
                    else:
                        edate = tseries
                    value = float(dt[1]) * multiplier
                    sql= "insert into series_%s values(%s,'%s',%d,-9,-9,-9);\n" % \
                    (ele,serid,tseries,value)
                    fout.write(sql)
                    i = i + 1
        except:
            fout.close()
            return 0,'',''
            
        fout.close()
        return 1,sdate,edate
    
    
    
    
    def proceed(self,*args,**kwargs):
        DATADIR = "C:\\ms4w\\Apache\\htdocs\\Symfony\\web\\uploads\\data"
        BUFFERDIR = "C:\\cherrypy\\buffer"
        f = open(os.path.join(_curdir,'serid.dat'),'r')
        serid = f.readline().strip()
        myserid = int(serid) + 1
        f.close()
        f = open(os.path.join(_curdir,'serid.dat'),'w')
        f.write('%d\n' % (myserid))
        f.close()
        reqid = kwargs['id']        
        c = cp.thread_data.db.cursor()
        sql = "select a.sta_id,b.ele_grp,a.path,a.user_id,a.elemen_id,a.processor_id \
        from datarequest a,elements b \
        where a.elemen_id=b.ele_id and req_id=" + reqid
        c.execute(sql)
        res = c.fetchone()
        staid = res[0]
        ele = res[1]
        infile = res[2]
        userid = res[3]
        eleid = res[4]
        procid = int(res[5])
        nmfileout="%s_%s_%s_%s.sql" % (reqid,serid,staid,ele)
        # ambil par_id
        #c = cp.thread_data.db.cursor()
        sql = "select sacad_id from mapusersacad where user_id=%s" % userid        
        c.execute(sql)
        res1 = c.fetchone()
        c.close()
        parid = res1[0]
        
        ret = 0
        # has implemented -> ADD
        # not yet implemented -> UPDATE
        if (procid==1):
            ret,sdate,edate = self.MWFklim(serid,eleid,ele,staid,parid,0,\
            os.path.join(DATADIR,infile),os.path.join(BUFFERDIR,nmfileout))
        
        elif (procid==2):
            pass
        
        tmpl = env.get_template('proceed.html')
        if (ret==1):
            curtimes = time.strftime("%Y-%m-%d %H:%M:%S")
            sql= "update datarequest set start_date='%s',end_date='%s',\
            ser_id=%s,status_id=1,process_date='%s' where req_id=%s" % (sdate,\
            edate,serid,curtimes,reqid)
            f_in, f_out = os.popen4('mysql -u dimas -pd1m4s dimasdb -e "%s"' % sql)
            #cxn = MySQLdb.connect(host='localhost', user = 'dimas',
            #                  passwd = 'd1m4s', db = 'dimasdb')
            #cursor = cxn.cursor()
            #cursor.execute (sql);
            #cursor.close();
            #c = cp.thread_data.db.cursor()
            #c.execute(sql)
            #c.close()
            message="Successfully ingested. Thank you for your contribution."
        else:
            message="Failed. Please consult with administrator."
		            
        
        return tmpl.render(mes=message)
    proceed.exposed = True








#======================================================================
if __name__ == '__main__':
	root = Root() #cp.config.update({'server.socket_port':9990})
	globalconf = {
             'global':{
			'engine.autoreload.on': False,
			'server.socket_host' : 'localhost',
			'server.socket_port' : 9090,
			'log.error_file': 'site.log',
                 'log.screen': True,
		}}
		
	appconf = {	
            '/screen.css':{
			'tools.staticfile.on': True,
			'tools.staticfile.filename': os.path.join(_curdir,'screen.css'),
		},
		'/dimas.js':{
			'tools.staticfile.on': True,
			'tools.staticfile.filename': os.path.join(_curdir,'dimas.js'),
		},
            '/datadir':{
			'tools.staticdir.on': True,
			'tools.staticdir.dir': 'C:\ms4w\Apache\htdocs\Symfony\web\uploads\data', #HARUS DI-SET
		},
            '/bufferdir':{
			'tools.staticdir.on': True,
			'tools.staticdir.dir': 'C:\ms4w\Apache\htdocs\Symfony\web\uploads\buffer', #HARUS DI-SET
		}
	}
	
	cp.config.update(globalconf)
	#cp.tree.mount(root,'/', config=appconf)
	#cp.server.quickstart()
	cp.quickstart(root,'/',appconf)
	cp.engine.start()
