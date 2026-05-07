from user.enums import DeviceTypes


def complete_device(type):
    if type == "web":
        return DeviceTypes.WEB
    elif type == "ios":
        return DeviceTypes.IOS
    elif type == "android":
        return DeviceTypes.ANDROID
