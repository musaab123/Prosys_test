--DROP FUNCTION get_pre_order_ids();
CREATE OR REPLACE FUNCTION public.update_rating_data(IN company_ids integer[])
RETURNS void AS
$BODY$
BEGIN
update setu_customer_score as cs
       set customer_rating_id =
      (select id from setu_customer_rating as cr
        where cs.total_score <= cr.to_score and
        cs.total_score >= cr.from_score and cs.company_id = cr.company_id and cs.company_id = any(company_ids));

insert into ir_property(fields_id,type,name,res_id,company_id)
(
select
	 	(select id from ir_model_fields where name = 'customer_rating_id' and model = 'res.partner')as field,
		'many2one' as type,'customer_rating_id' as name,
        concat('res.partner,',id)as res,
		company_id
     from
        (
			select
				id,
				company_id
			from
				(
				 select
				 id, unnest((select array_agg(distinct company_id) from setu_score_configuration where company_id = any(company_ids))) as company_id
				 from
				 res_partner
				)as pc
         where
            (id,company_id) not in
			(select
                        substring(res_id,13)::integer,company_id
                       from
                        ir_property
                       where
                        name = 'customer_rating_id' and company_id = any(company_ids) and
			 fields_id = (select id from ir_model_fields where name = 'customer_rating_id' and model = 'res.partner')
                        )

        )as IP
);

insert into ir_property(fields_id,type,name,res_id,company_id)
(
select
	 	(select id from ir_model_fields where name = 'total_score' and model = 'res.partner')as field,
		'integer' as type,'total_score' as name,
        concat('res.partner,',id)as res,
		company_id
     from
        (
			select
				id,
				company_id
			from
				(
				 select
				 id, unnest((select array_agg(distinct company_id) from setu_score_configuration where company_id = any(company_ids))) as company_id
				 from
				 res_partner
				)as pc
         where
            (id,company_id) not in
			(select
                        substring(res_id,13)::integer,company_id
                       from
                        ir_property
                       where
                        name = 'total_score' and company_id = any(company_ids) and
			 fields_id = (select id from ir_model_fields where name = 'total_score' and model = 'res.partner')
                        )

        )as IP
);

insert into ir_property(fields_id,type,name,res_id,company_id)
(
select
	 	(select id from ir_model_fields where name = 'customer_score_id' and model = 'res.partner')as field,
		'many2one' as type,'customer_score_id' as name,
        concat('res.partner,',id)as res,
		company_id
     from
        (
			select
				id,
				company_id
			from
				(
				 select
				 id, unnest((select array_agg(distinct company_id) from setu_score_configuration where company_id = any(company_ids))) as company_id
				 from
				 res_partner
				)as pc
         where
            (id,company_id) not in
			(select
                        substring(res_id,13)::integer,company_id
                       from
                        ir_property
                       where
                        name = 'customer_score_id' and company_id = any(company_ids) and
			 fields_id = (select id from ir_model_fields where name = 'customer_score_id' and model = 'res.partner')
                        )

        )as IP
);


update ir_property as ip
       set
         value_integer = ts.total_score
       from
         (
            select
                partner_id,
                company_id,
                total_score
            from setu_customer_score
         )as ts
         where
         ip.company_id = ts.company_id and
         ip.company_id = any(company_ids) and
         ip.res_id = concat('res.partner,',ts.partner_id) and
         ip.name = 'total_score' and
         ip.fields_id = (select id from ir_model_fields where name = 'total_score' and model = 'res.partner');

update ir_property as ip
       set
         value_reference = pr.rating
       from
       (
            select
                partner_id,
                company_id,
                case when customer_rating_id is not null
                then concat('setu.customer.rating,',customer_rating_id)
                else
                null
                end
                as rating
            from
                setu_customer_score cs
       )as pr
         where
         ip.company_id = pr.company_id and
         ip.company_id = any(company_ids) and
         ip.res_id = concat('res.partner,',pr.partner_id) and
         ip.name = 'customer_rating_id' and
         ip.fields_id = (select id from ir_model_fields where name = 'customer_rating_id' and model = 'res.partner');

update ir_property as ip
       set
         value_reference = cs.score
       from
       (
            select
                partner_id,
                company_id,
                case when id is not null
                then concat('setu.customer.score,',id)
                else
                null
                end
                as score
            from
                setu_customer_score cs
       )as cs
         where
         ip.company_id = cs.company_id and
         ip.company_id = any(company_ids) and
         ip.res_id = concat('res.partner,',cs.partner_id) and
         ip.name = 'customer_score_id' and
         ip.fields_id = (select id from ir_model_fields where name = 'customer_score_id' and model = 'res.partner');




END; $BODY$
LANGUAGE plpgsql VOLATILE
COST 100;
