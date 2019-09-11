import usb1 as usb
import gui_elements as gui
import device_operations as dops

def test_device(device_handle, port_number):    
        print('>>Device testing initiated.')

        _device = device_handle.getDevice()

        if unplugging_test(_device,  port_number) != None:
                print('Test 0 passed.')
                print('Device interface was claimed.')

def unplugging_test(_device, port_number):
    device_vendor_id = _device.getVendorID()
    device_product_id = _device.getProductID()
    device_bcd_number = _device.getbcdDevice()

    for i in range(4):
    
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

    def io_testing(device_handle):
        data = device_handle.bulkRead(,1024)