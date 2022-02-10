import argparse  #gerekli olan kütüphaneyi ekliyoruz

ap = argparse.ArgumentParser() # argüman çözücüyü ap değişkenine tanımladık

ap.add_argument("-n", "--name", required = True, help="name of the user") # ap değişkeninin tanımlı olduğu argparse.ArgumentParser() in içi boştu ve biz oraya veri ekledik
ap.add_argument("-s", "--surname", required = True, help="name of the user") # ap değişkeninin tanımlı olduğu argparse.ArgumentParser() in içi boştu ve biz oraya veri ekledik


args = vars(ap.parse_args()) #  ap.add_arguemnt ile kullanıcıdan aldığımız argümanları args değişkeninde tuttuk

print("Hi there {} {}, it's nice to see you!".format(args["name"],args["surname"])) # son olarak kullanıcıdan aldığımız argümanları kullanarak kullanıcıyı karşıladık

