#!/usr/bin/env bash
mongoexport  -d qianzhan -c company_info_export -f company_name,business_type,province,x_updatetime,operating_period,legal_representative,x_label,item_from,registration_authority,registered_capital,business_address,sort,business_scope,organization_registration_code,x_register_date,email,x_sign,register_date,business_status,x_status,registration_number,phone -q '{phone:{$exists:1}}' -o test.json

mongoimport --db qianzhan --collection company_info_export --file test.json