
import tornado.web
import tornado.ioloop

class basicRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world!!!!!!")

class resourceRequestHandler(tornado.web.RequestHandler):
    def get(self, id):
        self.write("Querying tweet with id " + id)

class queryStringRequestHandler(tornado.web.RequestHandler):
    def get(self):
	
        n = int(self.get_argument("n"))
        print("android request number " + str(n)) 
        r = "odd" if n % 2 else "even"
        
        self.write("the number " + str(n) + " is " + r)

class staticRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

# joystick request handler, posts joystick angle and strength to server
class joystickRequestHandler(tornado.web.RequestHandler):

    def get(self):
        left_angle = float(self.get_argument("leftAngle"))
        left_strength = float(self.get_argument("leftStrength"))
        right_angle = float(self.get_argument("rightAngle"))
        right_strength = float(self.get_argument("rightStrength"))

        print('joystick request received')

        joystick_dict = {
            'left_joystick': {'leftAngle': left_angle, 'leftStrength': left_strength},
            'right_joystick': {'rightAngle': right_angle, 'rightStrength': right_strength}
            }

        self.write(joystick_dict)

class joystickLeftRequestHandler(tornado.web.RequestHandler):

    def get(self):
        left_angle = float(self.get_argument("leftAngle"))
        left_strength = float(self.get_argument("leftStrength"))

        print('joystick request received')

        joystick_dict = {
            'left_joystick': {'leftAngle': left_angle, 'leftStrength': left_strength}
            }

        self.write(joystick_dict)

class joystickRightRequestHandler(tornado.web.RequestHandler):

    def get(self):
        right_angle = float(self.get_argument("rightAngle"))
        right_strength = float(self.get_argument("rightStrength"))

        print('joystick request received')

        joystick_dict = {
            'right_joystick': {'rightAngle': right_angle, 'rightStrength': right_strength}
            }

        self.write(joystick_dict)
        

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", basicRequestHandler),
        (r"/blog", staticRequestHandler),
        (r"/isEven", queryStringRequestHandler),
        (r"/tweet/([0-9]+)", resourceRequestHandler),
        (r"/joystick", joystickRequestHandler),
        (r"/joystick_left", joystickLeftRequestHandler),
        (r"/joystick_right", joystickRightRequestHandler)
    ])

    app.listen(1500)
    print("I'm listening on port 1500")
    tornado.ioloop.IOLoop.current().start()
