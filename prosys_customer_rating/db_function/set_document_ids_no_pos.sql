CREATE OR REPLACE FUNCTION public.set_document_ids_no_pos(
    IN company_ids integer[],
    IN date_limit date,
    IN invoice_due_date_limit date
)
RETURNS void AS
$BODY$
BEGIN

delete from average_sale_rel where score_id in (select score_id from setu_customer_score where company_id = any(company_ids));
insert into average_sale_rel(score_id,sale_id)
(select id as score_id,unnest(cus_score_data.sale_ids) from setu_customer_score as cs
inner join
(Select
	    Case When rp.parent_id is null
                               THEN rp.id
                               ELSE rp.parent_id
                           END as partner,
	    so.company_id,
	    array_agg(so.id) as sale_ids
	From sale_order so
	inner join res_partner rp on rp.id = so.partner_id
	where so.date_order >= date_limit and
	so.state in ('sale','done') GROUP BY partner,so.company_id)cus_score_data
on cs.partner_id = cus_score_data.partner and cs.company_id = cus_score_data.company_id and cus_score_data.company_id = any(company_ids));

delete from customer_score_unpaid_after_60_days_invoice_rel where score_id in (select score_id from setu_customer_score where company_id = any(company_ids));
insert into customer_score_unpaid_after_60_days_invoice_rel(score_id,invoice_id)
(select id as score_id,unnest(ids) from setu_customer_score as cs
inner join
(select
	Case When rp.parent_id is null
                               THEN rp.id
                               ELSE rp.parent_id
                           END as partner,
	ai.company_id,
	array_agg(ai.id)as ids
		from account_move as ai
		inner join res_partner rp on rp.id = ai.partner_id
		where
			ai.payment_state = 'not_paid' and
			ai.invoice_date >= date_limit and
			ai.move_type='out_invoice'
			and invoice_due_date_limit >= invoice_date_due and
			ai.invoice_date >= date_limit
		group by
		partner,
		ai.company_id
)due_after_days on due_after_days.partner = cs.partner_id and cs.company_id = due_after_days.company_id and due_after_days.company_id = any(company_ids));

delete from customer_score_refund_invoice_rel where score_id in (select score_id from setu_customer_score where company_id = any(company_ids));
insert into customer_score_refund_invoice_rel(score_id,invoice_id)
(select id as score_id,unnest(ids)as id from setu_customer_score as cs
inner join
(select
    Case When rp.parent_id is null
                               THEN rp.id
                               ELSE rp.parent_id
                           END as partner,
    cn.company_id,
	cn.ids
 from

    (select
        distinct ai.partner_id,
        ai.company_id,
        array_agg(distinct ai.id) as ids
	from account_move as ai
		right join account_move as air on air.id = ai.reversed_entry_id
		right join account_move_line as ail on ail.move_id = air.id
		right join sale_order_line_invoice_rel as rel on ail.id = rel.invoice_line_id
		right join sale_order_line as sol on rel.order_line_id = sol.id
		right join sale_order as so on sol.order_id = so.id
			where
				ai.payment_state in ('paid','in_payment','reversed','partial') and
				ai.move_type = 'out_refund' and
				so.state in ('sale','done') and
				ai.invoice_date >= date_limit
				GROUP BY ai.partner_id,ai.company_id
				)cn
				inner join res_partner rp on rp.id = cn.partner_id
)credit_notes on credit_notes.partner = cs.partner_id and credit_notes.company_id = cs.company_id and credit_notes.company_id = any(company_ids));

delete from customer_score_paid_after_due_invoice_rel where score_id in (select score_id from setu_customer_score where company_id = any(company_ids));
insert into customer_score_paid_after_due_invoice_rel (score_id,invoice_id)
(select id as score_id,unnest(invoice_done_after_due) from setu_customer_score
inner join (select Case When rp.parent_id is null
                               THEN rp.id
                               ELSE rp.parent_id
                           END as partner,
                           vals.company_id,
       array_agg(vals.id) as invoice_done_after_due From
                   (select
                        ai.partner_id,
                        ai.company_id,
                        ai.id,
                        ai.amount_total

					from account_move as ai
						where
							ai.payment_state in ('paid','in_payment','reversed','partial')
							and ai.move_type='out_invoice'
							and ai.invoice_date >= date_limit
							and (select invoice_date_due from account_move where id = ai.id)::date
							     <
							    (SELECT
								 					max(date)
								 				from
												(SELECT
                                                    max(move.date) as date
                                                FROM account_move move
                                                JOIN account_move_line line ON line.move_id = move.id
                                                JOIN account_partial_reconcile part ON
                                                    part.debit_move_id = line.id
                                                    OR
                                                    part.credit_move_id = line.id
                                                JOIN account_move_line counterpart_line ON
                                                    part.debit_move_id = counterpart_line.id
                                                    OR
                                                    part.credit_move_id = counterpart_line.id
                                                JOIN account_move invoice ON invoice.id = counterpart_line.move_id
                                                JOIN account_account account ON account.id = line.account_id
                                                WHERE account.account_type IN ('asset_receivable', 'liability_payable')
                                            AND invoice.id in (ai.id)
                                                    AND line.id != counterpart_line.id
                                                    AND invoice.move_type in ('out_invoice')
                                                GROUP BY move.date)as dates)::date

				group by ai.partner_id,ai.id,ai.company_id

			)as vals
			 inner join res_partner rp on rp.id = vals.partner_id
			 group by partner,vals.company_id)invoice_data on invoice_data.partner = setu_customer_score.partner_id and invoice_data.company_id = setu_customer_score.company_id
and invoice_data.company_id = any(company_ids)
);

END; $BODY$
LANGUAGE plpgsql VOLATILE
COST 100;

