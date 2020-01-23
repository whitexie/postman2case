from postman2case.core import PostmanParser
import logging

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    output_dir = '.'
    postman_parser = PostmanParser('./tests/data/open_wechat.postman_collection.json')
    output_file_type = 'yaml'

    parse_result = postman_parser.parse_data()
    postman_parser.save(parse_result, output_dir, output_file_type=output_file_type)

