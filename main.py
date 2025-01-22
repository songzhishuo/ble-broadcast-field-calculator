
data = "0201061AFF4C00021523A01DF0232A45989C0E393FB773F5BF3F877607BF07030408883F23AD0A09427274426561636F6E"

def parse_ble_advertising_data(data):
    parsed_data = []
    index = 0
    
    while index < len(data):
        # 解析长度字段（以字节为单位），长度包括字段长度本身
        length = int(data[index:index+2], 16)
        index += 2
        
        if length == 0:
            break
        
        # 解析类型字段
        field_type = data[index:index+2]
        index += 2
        
        # 解析值字段
        value_length = (length - 1) * 2  # 减去1以去掉类型字段
        value = data[index:index+value_length]
        index += value_length
        
        # 将解析后的字段添加到结果列表中
        parsed_data.append({
            'LEN': length,
            'TYPE': field_type,
            'VALUE': value
        })
    
    return parsed_data    

def split_data_by_length(parsed_data, threshold=31):
    """根据字段长度将数据分为两个字段"""
    field1 = ""
    field2 = ""
    length_accumulated = 0
    field1_length = 0

    for field in parsed_data:
        field_length = field['LEN']
        field_value = field['VALUE']
        field_type = field['TYPE']
        # print("Fied:-->", field)

        # 检查累积长度是否超过阈值
        if field1_length + (field_length+1) <= threshold:
            # field1 += field_value
            # temp_str = field['LEN'] + field['TYPE'] + field['VALUE']
            field1 += f"{field_length:02X}"#str(field_length)
            # field1 += f"{field_type:02X}"#str(field_type)
            field1 += str(field_type)
            field1 += field_value

            field1_length += field_length + 1
        else:
            # field2 += field_value
            # field['LEN'] + field['TYPE'] + field['VALUE']
            # temp_str = field['LEN'] + field['TYPE'] + field['VALUE']
            field2 += f"{field_length:02X}"#str(field_length)
            field2 += str(field_type)
            field2 += field_value
            
    return field1, field2

def format_hex_string(data):
    """格式化十六进制字符串以便于查看"""
    return ' '.join(data[i:i+2] for i in range(0, len(data), 2))

def format_c_style_array(hex_string):
    """将十六进制字符串转换为C风格的字节数组形式"""
    # 先将字符串中的空格移除
    hex_string = hex_string.replace(" ", "")
    # 每两个字符组成一个字节，并加上C语言的字节数组格式
    byte_list = [f"0x{hex_string[i:i+2]}" for i in range(0, len(hex_string), 2)]
    # 将字节列表转换为C风格的数组字符串
    c_array = ", ".join(byte_list)
    return f"unsigned char data[] = {{{c_array}}};"

if __name__ == "__main__":
    # 示例数据段

    # 解析数据
    parsed_data = parse_ble_advertising_data(data)
    # print("----:", parsed_data)
    # 按字段长度分割数据
    field1, field2 = split_data_by_length(parsed_data)
    
    # 打印结果
    print(f"字段1：{format_hex_string(field1)}")
    print(f"字段2：{format_hex_string(field2)}")

    # 打印C风格的数组
    print("广播字段 C风格数组：")
    print(format_c_style_array(format_hex_string(field1)))
    print("响应字段 C风格数组：")
    print(format_c_style_array(format_hex_string(field2)))

# 02    01  06                                                                      --- 
# 1A    FF  4C00021523
#           A01DF0232A
#           45989C0E39
#           3FB773F5BF
#           3F87728CBF

# 07    03  BF04883F23AD
# 0A    09  427274426561636F6E
