# 模拟登陆知乎

知乎登录页改版之后，原来的登陆方法失效。改版后的登陆难度增大，在于signature参数的获取。
signature参数获取方式：

`def get_signature(self):  `
        
        myhmac = hmac.new(self.key, None, 'sha1')
        myhmac.update(bytes(self.form_data['grant_type'], 'utf-8'))  
        myhmac.update(bytes(self.form_data['client_id'], 'utf-8'))  
        myhmac.update(bytes(self.form_data['source'], 'utf-8'))
        myhmac.update(bytes(self.form_data['timestamp'], 'utf-8'))  
        return myhmac.hexdigest()
