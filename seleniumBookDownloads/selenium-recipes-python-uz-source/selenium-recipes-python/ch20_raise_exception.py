import platform
print(platform.system())
if platform.system() != "Darwin":
  raise Exception("Unsupport platform: " + platform.system() )  
