import cherrypy as cp

class Root:
    islogin=False
    def index(self):
		fid = open("../testcherry.txt","w")
		fid.write("hahaha")
		fid.close()
		return "Hello world!"
    index.exposed = True

    def doLogin(self):
        login="""<form action="loginHandler" method="post">
                <p>Username</p>
                <input type="text" name="username" value=""
                size="15" maxlength="40"/>
                <p>Password</p>
                <input type="password" name="password" value=""
                size="10" maxlength="40"/>
                <p><input type="submit" value="Login"/></p>
                <p><input type="reset" value="Clear"/></p>
                </form> """
        return login
    doLogin.exposed = True

    def loginHandler(self,username,password):
        return "login:%s password:%s handler return.." % (username,password)
    loginHandler.exposed = True

class Admin:
    def index(self):
        return "administrator page"
    index.exposed = True
    
if __name__ == '__main__':
    root = Root()
    root.admin = Admin()
    cp.config.update({'server.socket_port':9990})
    #cp.server.start()
    #cp.engine.block()
    cp.quickstart(root)
