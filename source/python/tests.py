import usb1 as usb
import gui_elements as gui
import device_operations as dops

def test_device(_device, port_number):    
        print('Device interface was claimed.')
        if unplugging_test(_device,  port_number):
                print("Test 0 passed.")

def unplugging_test(_device, port_number):
    device_vendor_id = _device.getVendorID()
    device_product_id = _device.getProductID()
    device_bcd_number = _device.getbcdDevice()

    for i in range(4):
        gui.show_msg_box('Guidline', 'Unlpug the USB device, click Okay and then plug it in tha same port.')

        while dops.find_by_port_number(port_number) is None:
            a = 0 #empty operation        
        _device = dops.find_by_port_number(port_number)

        test_vid = _device.getVendorID()
        test_pid = _device.getProductID()
        test_bcdn = _device.getbcdDevice()

        if test_vid != device_vendor_id or test_pid != device_product_id or test_bcdn != device_bcd_number:
            return False        
    return True