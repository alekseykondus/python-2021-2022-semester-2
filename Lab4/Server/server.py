from shop import Shop
import Pyro4

if __name__ == '__main__':
	daemon = Pyro4.Daemon()
	uri = daemon.register(Shop)
	ns = Pyro4.locateNS()
	ns.register('shop', uri)
	daemon.requestLoop()