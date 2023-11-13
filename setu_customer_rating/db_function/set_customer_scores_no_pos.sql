CREATE OR REPLACE FUNCTION public.set_customer_scores_no_pos(
    IN company_ids integer[],
    IN date_limit date,
    IN months numeric,
    IN invoice_due_date_limit date,
    IN score_conf_avg_sales_amt_id numeric,
    IN score_conf_avg_monthly_sales_refund_id numeric,
    IN score_conf_qty_invoice_paid_after_due_id numeric,
    IN score_conf_amt_invoice_paid_after_due_id numeric,
    IN score_conf_qty_invoice_paid_after_x_days_id numeric,
    IN score_conf_amt_invoices_due_after_x_days_id numeric,
    IN score_conf_avg_payment_days_id numeric
)
RETURNS void AS
$BODY$

BEGIN


update setu_customer_score as cs
set
	avg_monthly_sales_score = cs2.avg_sales_score,
    avg_monthly_refund_score = cs2.avg_refund_score,
    qty_invoice_paid_score = cs2.due_date_qty,
    amount_invoice_paid_score = cs2.due_date_score_amt,
    qty_invoices_due_after_60_days_score = cs2.due_after_60_qty,
    amount_invoices_due_after_60_days_score = cs2.due_after_60_amt,
    average_payment_days_score = cs2.avg_pay_score,
    pre_sale_orders_canceled_score = cs2.pre_cancel_score,
    total_score = cs2.total_score,
    company_id = cs2.company_id


from
(
    select main_data.partner_id,
        main_data.avg_sales_score,
        main_data.avg_refund_score,
        main_data.due_date_score_amt,
        main_data.due_date_qty,
        main_data.due_after_60_amt,
        main_data.due_after_60_qty,
        main_data.pre_cancel_score,
        main_data.avg_pay_score,
        (
        main_data.avg_sales_score+
        main_data.avg_refund_score+
        main_data.due_date_score_amt+
        main_data.due_date_qty+
        main_data.due_after_60_amt+
        main_data.due_after_60_qty+
        main_data.pre_cancel_score+
        main_data.avg_pay_score
        )as total_score,
        main_data.company_id
        from
            (select
                data.partner_id,
                data.company_id,
                max(data.avg_sales_score)avg_sales_score,
                max(data.avg_refund_score)avg_refund_score,
                max(data.due_date_score_amt)due_date_score_amt,
                max(data.due_date_qty)due_date_qty,
                max(data.due_after_60_amt)due_after_60_amt,
                max(data.due_after_60_qty)due_after_60_qty,
                max(data.pre_cancel_score)pre_cancel_score,
                max(data.avg_pay_score)avg_pay_score
                from


                    (
                    select
                        id as partner_id,
                        company_id as company_id,
                        0 as avg_sales_score,
                        0 as avg_refund_score,
                        0 as due_date_score_amt,
                        0 as due_date_qty,
                        0 as due_after_60_amt,
                        0 as due_after_60_qty,
                        0 as pre_cancel_score,
                        0 as avg_pay_score


                        from
                        (select
                            id,unnest((select array_agg(companies.id)
                            from (select distinct company_id as id from setu_score_configuration where company_id = any(company_ids) order by id)as companies))as company_id
                        from res_partner where parent_id is null)as partner_data

                    UNION

                        select
                           Case When rp.parent_id is null
                               THEN rp.id
                               ELSE rp.parent_id
                           END as partner_id,
                           partner_amount.company_id as company_id,
                           (select pre_score
                        from setu_score_configuration_line_price lin
                        inner join setu_score_configuration sc on sc.id = lin.score_conf_id
                        where sc.calculation_formula = 'avg_monthly_sales' and sc.company_id = partner_amount.company_id and
                        partner_amount.average_amount >= lin.from_price and partner_amount.average_amount <= lin.to_price) as avg_sales_score,
                           0 as avg_refund_score,
                           0 as due_date_score_amt,
                           0 as due_date_qty,
                           0 as due_after_60_amt,
                           0 as due_after_60_qty,
                           0 as pre_cancel_score,
                           0 as avg_pay_score

                           from
                        (
                        --from
                        select
                        sales.partner_id,
                        sales.company_id,
                        sum(average_amount) as average_amount
                        from
                            (Select
                                Case When rp.parent_id is null
									   THEN rp.id
									   ELSE rp.parent_id
								   END as partner_id,
							 	so.company_id,
                                 sum(
                                 case when so.currency_id = com.currency_id
								 then
								 so.amount_total
								 else
								 round((so.amount_total / coalesce(so.currency_rate,1)),2)
								 end
								 )/months as average_amount

                            From sale_order so
							 inner join res_partner rp on rp.id = so.partner_id
                            inner join res_company com on com.id = so.company_id

                            where date_order >= date_limit
                            and state in ('sale','done') GROUP BY rp.id,rp.parent_id,so.company_id

							)as sales
							where sales.company_id = any(company_ids)

                        group by sales.partner_id,sales.company_id
                        --to
                        )as partner_amount
                        Inner Join res_partner rp on rp.id = partner_amount.partner_id


                    UNION
                        select
                        Case When rp.parent_id is null
                               THEN rp.id
                               ELSE rp.parent_id
                           END as partner_id,
                        values.company_id as company_id,
                        0 as avg_sales_score,
                        0 as avg_refund_score,
                        (
                        select pre_score
                        from setu_score_configuration_line_price lin
                        inner join setu_score_configuration sc on sc.id = lin.score_conf_id
                        where sc.calculation_formula = 'amt_invoice_paid' and sc.company_id = values.company_id and
                        values.amount >= lin.from_price and values.amount <= lin.to_price
                        ) as due_date_score_amt,
                        (select pre_score
                        from setu_score_configuration_line_qty lin
                        inner join setu_score_configuration sc on sc.id = lin.score_conf_id
                        where sc.calculation_formula = 'qty_invoice_paid' and sc.company_id = values.company_id and
                        values.qty >= lin.from_quantity and values.qty <= lin.to_quantity) as due_date_qty,
                        0 as due_after_60_amt,
                        0 as due_after_60_qty,
                        0 as pre_cancel_score,
                        0 as avg_pay_score
                        from

                            (select
                            vals.partner_id,
                            vals.company_id,
                            max(vals.amount) as amount,
                            max(vals.qty) as qty
                            from

                                (
                                select
                                 Case When rp.parent_id is null
								   THEN rp.id
								   ELSE rp.parent_id
							   	 END as partner_id,
                                paid_invoices.company_id,
                                 0 as amount,
                                 0 as qty
                                From

                                (select
                                ai.partner_id,
                                ai.id,ai.name,
                                ai.company_id,
                                ai.amount_total
                                from account_move as ai
                                where ai.payment_state in ('paid','in_payment','reversed','partial')
                                and ai.move_type='out_invoice'
                                and ai.invoice_date >= date_limit
                                ) as paid_invoices
									  Inner Join res_partner rp on rp.id = paid_invoices.partner_id


                                where
                                (select invoice_date_due from account_move where id = paid_invoices.id)::date >=
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
                                                    --AND payment.id IN %(payment_ids)s
                                            AND invoice.id in (paid_invoices.id)
                                                    AND line.id != counterpart_line.id
                                                    AND invoice.move_type in ('out_invoice')
                                                GROUP BY move.date)as dates)
                                group by rp.id,rp.parent_id, paid_invoices.company_id


                                UNION

                                select
									 Case When rp.parent_id is null
								   THEN rp.id
								   ELSE rp.parent_id
							   	 END as partner_id,
									vals.company_id,
                                 	sum(vals.amount_total) as amount,
                                 	count(vals.id) as qty From
                                    (select
                                        ai.partner_id,
                                        ai.company_id,
                                        ai.id,
                                        case when ai.currency_id = com.currency_id
                                         then
                                         ai.amount_total
                                         else
                                         round((ai.amount_total / coalesce((select rate from get_nearest_currency_rate(ai.invoice_date::date,ai.company_id) where currency_id = ai.currency_id),1)),2)
                                         end as amount_total



                                    from account_move as ai
                                    inner join res_company com on com.id = ai.company_id

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
                                                GROUP BY move.date)as dates)


                                    )as vals
									inner join res_partner rp on rp.id = vals.partner_id
									group by rp.id,rp.parent_id,vals.company_id
                                	)as vals group by vals.partner_id,vals.company_id
                            )as values
                            Inner Join res_partner rp on rp.id = values.partner_id
                            where values.company_id = any(company_ids)

                    UNION
                    --Another one
                        select
                        Case When rp.parent_id is null
                               THEN rp.id
                               ELSE rp.parent_id
                           END as partner_id,
                        invoice_data.company_id as company_id,
                        0 as avg_sales_score,
                        0 as avg_refund_score,
                        0 as due_date_score_amt,
                        0 as due_date_qty,

                        (
                        select pre_score
                        from setu_score_configuration_line_price lin
                        inner join setu_score_configuration sc on sc.id = lin.score_conf_id
                        where sc.calculation_formula = 'amt_invoice_due' and sc.company_id = invoice_data.company_id and
                        total_amount >= lin.from_price and total_amount <= lin.to_price
                        ) as due_after_60_amt,
                        (select pre_score
                        from setu_score_configuration_line_qty lin
                        inner join setu_score_configuration sc on sc.id = lin.score_conf_id
                        where sc.calculation_formula = 'qty_invoice_due' and sc.company_id = invoice_data.company_id and
                        total_qty >= lin.from_quantity and total_qty <= lin.to_quantity) as due_after_60_qty,

                        0 as pre_cancel_score,
                        0 as avg_pay_score

                        from
                        (select
                            invs_data.partner,invs_data.company_id,
                            max(invs_data.total_amount)as total_amount,
                            max(invs_data.total_qty)as total_qty

                            from
                                (       select
                                       	Case When rp.parent_id is null
										   THEN rp.id
										   ELSE rp.parent_id
									   END as partner,
								 		 ai.company_id,
                                        0 as total_amount,
                                        0 as total_qty

                                        from


                                        (select partner_id,company_id
                                        from account_move as ai

                                        where
                                            ai.payment_state in ('paid','in_payment','reversed','partial') and
                                            ai.invoice_date >= date_limit and
                                            ai.move_type='out_invoice')as ai
								        inner join res_partner rp on rp.id = ai.partner_id
                                        group by partner,ai.company_id

                                    UNION

                                    select
                                        Case When rp.parent_id is null
										   THEN rp.id
										   ELSE rp.parent_id
									   END as partner,
                                        ai.company_id,
                                        sum(case when ai.currency_id = com.currency_id
                                             then
                                             ai.amount_total
                                             else
                                             round((ai.amount_total / coalesce((select rate from get_nearest_currency_rate(ai.invoice_date::date,ai.company_id) where currency_id = ai.currency_id),1)),2)
                                             end) as total_amount,
                                        count(ai.id) as total_qty

                                            from account_move as ai
                                            inner join res_partner rp on rp.id = ai.partner_id
                                            inner join res_company com on com.id = ai.company_id
                                            where
                                                ai.payment_state = 'not_paid' and
                                                ai.invoice_date >= date_limit and
                                                ai.move_type='out_invoice'
                                                and invoice_due_date_limit >= invoice_date_due
                                            group by partner,ai.company_id
                                ) as invs_data
                                group by invs_data.partner,invs_data.company_id
                                )as invoice_data
                                Inner Join res_partner rp on rp.id = invoice_data.partner
                                where invoice_data.company_id = any(company_ids)

                    UNION
                        select
                        Case When rp.parent_id is null
                               THEN rp.id
                               ELSE rp.parent_id
                           END as partner_id,
                        avg_pay_dates.company_id as company_id,
                        0 as avg_sales_score,
                        0 as avg_refund_score,
                        0 as due_date_score_amt,
                        0 as due_date_qty,
                        0 as due_after_60_amt,
                        0 as due_after_60_qty,
                        0 as pre_cancel_score,
                        case when avg_pay_dates.avg_days <= 0 then (select max(pre_score)
                        from setu_score_configuration_line_qty lin
                        inner join setu_score_configuration sc on sc.id = lin.score_conf_id
                        where sc.calculation_formula = 'avg_payment_days' and sc.company_id = avg_pay_dates.company_id)
                        else (select pre_score
                        from setu_score_configuration_line_qty lin
                        inner join setu_score_configuration sc on sc.id = lin.score_conf_id
                        where sc.calculation_formula = 'avg_payment_days' and sc.company_id = avg_pay_dates.company_id and
                        avg_days >= lin.from_quantity and avg_days <= lin.to_quantity)
                        end avg_pay_score

                        from
                        (select
                            subject_id as partner_id,
                            company_id,
                            avg(pay_days) as avg_days
                         from
                            (
                            SELECT
                                invoice.partner_id,
                                Case When rp.parent_id is null
                                   THEN rp.id
                                   ELSE rp.parent_id
                                END as subject_id,
								invoice.company_id,
                                move.date - invoice.invoice_date as pay_days
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
                            INNER JOIN res_partner rp on rp.id = invoice.partner_id
                            JOIN account_account account ON account.id = line.account_id
                            WHERE account.account_type IN ('asset_receivable', 'liability_payable')
                                AND line.id != counterpart_line.id
                                AND invoice.move_type in ('out_invoice')
                                AND invoice.payment_state in ('paid','in_payment','reversed','partial')
                             --group by invoice.partner_id,subject_id,invoice.company_id
                             )as apd
                         group by apd.subject_id,company_id
                        )as avg_pay_dates

                             Inner Join res_partner rp on rp.id = avg_pay_dates.partner_id
                        where avg_pay_dates.company_id = any(company_ids)


                    UNION

                        select
                        partner_percentage.partner_id as partner_id,
                        partner_percentage.company_id as company_id,
                        0 as avg_sales_score,
                        case when partner_percentage.refund_percentage = 0 then
                        (select max(pre_score) from setu_score_configuration_line_percentage line inner join setu_score_configuration sc on sc.id = line.score_conf_id where sc.company_id = partner_percentage.company_id)
                        ELSE
                        (select pre_score from setu_score_configuration_line_percentage line
                        inner join setu_score_configuration sc on sc.id = line.score_conf_id
                        where sc.company_id = partner_percentage.company_id and
                        partner_percentage.refund_percentage >= from_percentage
                                    and
                        partner_percentage.refund_percentage <= to_percentage) END avg_refund_score,
                        0 as due_date_score_amt,
                        0 as due_date_qty,
                        0 as due_after_60_amt,
                        0 as due_after_60_qty,
                        0 as pre_cancel_score,
                        0 as avg_pay_score
                        from
                            (select

                                partner_id,
                                company_id,
                                max(refund_percentage)as refund_percentage
                            from
                                    (
                                    --from here
                                    select
                                        distinct partner_id,
										company_id,
                                        0 as refund_percentage
                                         from (select
                                                        Case When rp.parent_id is null
                                                               THEN rp.id
                                                               ELSE rp.parent_id
                                                           END as partner_id,
											   			am.company_id

                                                            from account_move am
                                                            Inner Join res_partner rp on rp.id = am.partner_id
                                                            where
                                                            am.invoice_date >= date_limit and
                                                            am.payment_state in ('paid','in_payment','reversed','partial')
                                               )as inv

                                    UNION
                                        Select
                                        partner_id,
                                        company_id,
                                        case when sales_average > 0 then (refund_average*100)/sales_average
										    else 100 end as refund_percentage
										From
                                                (select partner_id,company_id,sum(refund_average)refund_average,sum(sales_average)sales_average from
                                                (
													select partner as partner_id,company_id,max(refund_average)refund_average,max(sales_average)sales_average from
                                                    (
                                                    select
                                                        Case When rp.parent_id is null
                                                               THEN rp.id
                                                               ELSE rp.parent_id
                                                           END as partner,
                                                        ram.company_id,
                                                        sum(
                                                        case when ram.currency_id = com.currency_id
                                                        then
                                                        abs(ram.amount_total)
                                                        else
                                                          round(abs(ram.amount_total) / coalesce(
                                                                                        (select
                                                                                            rate
                                                                                         from
                                                                                            get_nearest_currency_rate(ram.invoice_date::date,ram.company_id)
                                                                                         where currency_id = ram.currency_id
                                                                                        ),1),2)
                                                        end
                                                        ) as refund_average,
                                                        0 as sales_average
                                                    from

													(select distinct ai.id
													from account_move as ai
                                                    inner join account_move as air on air.id = ai.reversed_entry_id
                                                    inner join account_move_line as ail on ail.move_id = air.id
                                                    inner join sale_order_line_invoice_rel as rel on ail.id = rel.invoice_line_id
                                                    inner join sale_order_line as sol on rel.order_line_id = sol.id
                                                    inner join sale_order as so on sol.order_id = so.id
                                                    where
                                                    ai.payment_state in ('paid','in_payment','reversed','partial') and
                                                    ai.move_type = 'out_refund' and
                                                    so.state in ('sale','done') and
                                                    ai.invoice_date >= date_limit)as ri

													inner join account_move ram on ram.id = ri.id
													inner join res_partner rp on rp.id = ram.partner_id
													inner join res_company com on com.id = ram.company_id
													group by partner,ram.company_id

                                                    UNION

                                                   select
                                                    Case When rp.parent_id is null
                                                               THEN rp.id
                                                               ELSE rp.parent_id
                                                           END as partner,
                                                    sub.company_id,
                                                    sum(sub.refund_average) as refund_average,
                                                    sum(case when sub.so_cur = sub.com_cur
                                                         then
                                                         abs(sub.amount_total)
                                                         else
                                                         round((abs(sub.amount_total) / coalesce(sub.currency_rate,1)),2)end

                                                        ) as sales_average
                                                    from
                                                    (
                                                        SELECT
                                                            so.partner_id,
                                                            so.company_id,
                                                            0 as refund_average,
                                                            max(so.amount_total) as amount_total,
                                                            max(so.currency_rate) as currency_rate,
                                                            max(so.currency_id) as so_cur,
                                                            max(com.currency_id) as com_cur
                                                        from sale_order so
                                                        inner join sale_order_line sol on sol.order_id = so.id
                                                        inner join sale_order_line_invoice_rel rel on rel.order_line_id = sol.id
                                                        inner join account_move_line aml on aml.id = rel.invoice_line_id
                                                        inner join account_move am on am.id = aml.move_id
                                                        inner join res_company com on com.id = so.company_id
                                                        where
                                                            so.state in ('sale','done') and
                                                            so.date_order >= date_limit and
                                                            am.payment_state in ('paid','in_payment','reversed','partial')

                                                        group by
                                                            so.partner_id,so.company_id,so.id
                                                    )sub
                                                    Inner Join res_partner rp on rp.id = sub.partner_id
									                group by partner,sub.company_id
                                                    )as refund_and_sales_date group by partner_id,refund_and_sales_date.company_id


												)as mid_data
                                                 group by mid_data.partner_id,mid_data.company_id
                                                )as a order by refund_percentage desc
                                )as invoice_partner_percentage_data group by partner_id,company_id
                                )as partner_percentage
                                where partner_percentage.company_id = any(company_ids)
                                group by partner_id,company_id,refund_percentage
                )as data
                group by data.partner_id,data.company_id
        )as main_data order by total_score desc
    )as cs2 where
     cs.partner_id = cs2.partner_id and
     cs.company_id = any(company_ids) and
     cs2.partner_id not in (select partner_id from score_to_create) and
     cs.company_id = cs2.company_id;


END; $BODY$
LANGUAGE plpgsql VOLATILE
COST 100;
