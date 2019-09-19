import usb1 as usb
import gui_elements as gui
import device_operations as dops
import data_provider

TESTS_RANGE = 4

def test_device(device_handle, port_number,context):    
        print('>> Device testing initiated.')

        device = device_handle.getDevice()

        if unplugging_test(device,  port_number) == False:
                return False
        print("> Test 0 was passed.")

        if detect_device_type_test(device_handle) == False:
            print("> Test 1 failed.")
            return False
        
        print("> Test 1 was passed.")

        return True

def unplugging_test(_device, port_number):
    device_vendor_id = _device.getVendorID()
    device_product_id = _device.getProductID()
    device_bcd_number = _device.getbcdDevice()

    for i in range(TESTS_RANGE):
    
        # the following two lines will be optimised when suitable hardware is present
        while dops.find_by_port_number(port_number) is None:
            a = 0 #empty operation        

        _device = dops.find_by_port_number(port_number)

        test_vid = _device.getVendorID()
        test_pid = _device.getProductID()
        test_bcdn = _device.getbcdDevice()

        if test_vid != device_vendor_id or test_pid != device_product_id or test_bcdn != device_bcd_number:
            return False

        #the following line will be removed as part of optimisation when suitable harware is present    
        gui.show_msg_box('Guidline', 'Unlpug the USB device, click Okay and then plug it in tha same port.')

    return True

def detect_device_type_test(device_handle):
    device = device_handle.getDevice()
    
    dev_configuration = next(device.iterConfigurations())
    dev_descriptor_id = next(dev_configuration.__getitem__(0).__iter__()).getSubClass()

    if dev_descriptor_id != 6 or dev_configuration.getNumInterfaces() > 1:
        return False
    return True
    
def io_lightweight_testing(device_handle):
    device = device_handle.getDevice()

    for i in range(TESTS_RANGE):
        
        #pseudorandomly generates a string with a given length
        test_string = data_provider.generate_pseudorandom_string(64)

        dops.handle_kernel_driver(device_handle)                

        #if received_data != test_string:
        return False

    return True