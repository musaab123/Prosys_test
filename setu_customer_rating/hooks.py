from odoo import api, SUPERUSER_ID


def create_rating_table(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    company_id = env.ref('base.main_company')
    company = env['setu.customer.rating.company'].create({
        'company_id': company_id.id
    })
    env['setu.customer.rating'].with_context(let_me_create=True).create({
        'company_id': company_id.id,
        'from_score': 0,
        'to_score': 25,
        'rating': 'C',
        'crc_id': company.id
    })
    env['setu.customer.rating'].with_context(let_me_create=True).create({
        'company_id': company_id.id,
        'from_score': 26,
        'to_score': 50,
        'rating': 'B',
        'crc_id': company.id
    })
    env['setu.customer.rating'].with_context(let_me_create=True).create({
        'company_id': company_id.id,
        'from_score': 51,
        'to_score': 75,
        'rating': 'A',
        'crc_id': company.id
    })

    env['setu.customer.rating'].with_context(let_me_create=True).create({
        'company_id': company_id.id,
        'from_score': 76,
        'to_score': 100,
        'rating': 'AAA',
        'crc_id': company.id
    })
