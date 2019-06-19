from flask_restful import Resource, reqparse, request
from app.helpers.rest import response
from app.helpers import cmd_parser as cmd
from app import psycopg2,db
from app.libs import util as utils
from app.models import model



class CompanyProducts(Resource):

    def get(self):
        command = utils.get_command(request.path)
        command = "dt_"+command
        try:
            results = model.get_all(command)
            obj_userdata = list()
            for i in results:
                data = {
                    "id_company_product": str(i['id_company_product']),
                    "id_company": str(i['id_company']),
                    "id_product": str(i['id_product']),
                    "id_worker": str(i['id_worker']),
                    "nm_company_product": str(i['nm_company_product'])
                }
                obj_userdata.append(data)
        except Exception:
            results = None
        else:
            return response(200, data=obj_userdata)

    def post(self):
        json_req = request.get_json(force=True)
        command = utils.get_command(request.path)
        command = 'dt_'+command
        init_data = cmd.parser(json_req, command)
        respons = {}
        if init_data['action'] == 'insert':
            table = init_data['data'][0]['table']
            fields = init_data['data'][0]['fields']
            try:
                result = model.insert(table, fields)
            except Exception as e:
                respons = {
                    "status": False,
                    "error": str(e)
                }
            else:
                respons = {
                    "status": True,
                    "messages": "Success",
                    "id": result
                }
            finally:
                return response(200, data=fields , message=respons)
        if init_data['action'] == 'remove':
            table = ""
            tags = dict()
            fields = ""
            for i in init_data['data']:
                table = i['table']
                tags = i['tags']
            fields = str(list(tags.keys())[0])
            try:
                result = model.delete(table, fields, tags[fields])
            except Exception as e:
                respons = {
                    "status": False,
                    "messages": str(e)
                }
            else:
                respons = {
                    "status": result,
                    "messages": "Success!"
                }
            finally:
                return response(200, data=tags, message=respons)
        if init_data['action'] == 'where':
            obj_userdata = list()
            table = ""
            fields = ""
            tags = dict()
            for i in init_data['data']:
                table = i['table']
                tags = i['tags']
                for a in tags:
                    if tags[a] is not None:
                        fields = a
            try:
                print(tags)
                result = model.get_by_id(table,fields,tags[fields])
            except Exception as e:
                respons = {
                    "status": False,
                    "messages": str(e)
                }
            else:
                for i in result :
                    data = {
                    "id_company_product": str(i['id_company_product']),
                    "id_company": str(i['id_company']),
                    "id_product": str(i['id_product']),
                    "id_worker": str(i['id_worker']),
                    "nm_company_product": i['nm_company_product']
                    }
                    obj_userdata.append(data)
                respons = {
                    "status": True,
                    "messages": "Fine!"
                }
            finally:
                return response(200, data=obj_userdata , message=respons)