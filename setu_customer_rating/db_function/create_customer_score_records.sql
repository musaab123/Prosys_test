--DROP FUNCTION get_invoice_due_after_x_days_ids();
CREATE OR REPLACE FUNCTION public.create_customer_score_records(
IN company_ids integer []
)
RETURNS void AS
$BODY$
BEGIN
Drop Table if exists score_to_create;
Create table score_to_create (
                            partner_id integer PRIMARY KEY,
                            company_id integer);

DELETE FROM score_to_create where company_id = any(company_ids) or company_id is null;
delete from setu_customer_score;

INSERT INTO setu_customer_score(partner_id,company_id)
select * from
(
    SELECT
        id,
        unnest((select array_agg(distinct company_id) from setu_score_configuration where company_id = any(company_ids)))as company_id
    FROM res_partner
    WHERE
        parent_id is null
)as partners
    WHERE (partners.id,partners.company_id) not in (select partner_id,company_id from setu_customer_score);

END; $BODY$
LANGUAGE plpgsql VOLATILE
COST 100;
