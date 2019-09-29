import usb1 as usb
from logger import log
import gui_elements as gui
import device_operations as dops
import data_provider
import pyudev

TESTS_RANGE = 4

def test_device(device_handle, port_number,context):
    log('>> Device testing initiated.')

    device = unplugging_test(device_handle.getDevice(),  port_number)

    if device == None:
        log("> Test 0 failed.")
        return False
    log("> Test 0 was passed.")
    
    if detect_device_type_test(device_handle) == False:
        log("> Test 1 failed.")
        return False
    log("> Test 1 was passed.")
    
    dops.handle_kernel_driver(device_handle)
    return True

def unplugging_test(_device, port_number):
    device_vendor_id = _device.getVendorID()
    device_product_id = _device.getProductID()
    device_bcd_number = _device.getbcdDevice()

    for i in range(TESTS_RANGE):
        #the following line will be removed as part of optimisation when suitable harware is present    
        gui.show_msg_box('Guidline', 'Unlpug the USB device, click Okay and then plug it in tha same port.')
        
        # the following two lines will be optimised when suitable hardware is present
        while dops.find_by_port_number(port_number) is None:
            a = 0 #empty operation        

        _device = dops.find_by_port_number(port_number)

        test_vid = _device.getVendorID()
        test_pid = _device.getProductID()
        test_bcdn = _device.getbcdDevice()

        if test_vid != device_vendor_id or test_pid != device_product_id or test_bcdn != device_bcd_number:
            return None

    return _device

def detect_device_type_test(device_handle):
    device = device_handle.getDevice()
    
    device_configuration = next(device.iterConfigurations())
    device_interface_class = next(device_configuration.__getitem__(0).__iter__()).getClass()

    if device_interface_class != 8 or device_configuration.getNumInterfaces() > 1:
        return False
    return True
    
    #unused function
def __io_lightweight_testing(self):    
    context = pyudev.Context()

    for dev in context.list_devices(DEVTYPE='disk'):
        dev_id = dev.get('ID_VENDOR_ID')
        print(dev_id)

        return True 