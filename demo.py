from postman2case.core import PostmanParser



if __name__ == '__main__':
    output_file_type = "json"
    output_dir = '.'
    postman_testcase_file = './tester_postman_collection.json'

    postman_parser = PostmanParser(postman_testcase_file)
    parse_result = postman_parser.parse_data()
    postman_parser.save(parse_result, output_dir, output_file_type=output_file_type)

