# -*- coding: utf-8 -*-

from openerp import tools
from openerp.osv import fields,osv

class report_stock_lot_rebut(osv.osv):
    _name = "report.stock.lot.rebut"
    _description = "stock des produits par lot"
    _auto = False
    _columns = {
        'product_id': fields.many2one('product.product', 'Article', readonly=True),
        'location_id': fields.many2one('stock.location', 'Emplacement', readonly=True),
        'qty': fields.float(u'Quantité', readonly=True),
        'lot_id': fields.many2one('stock.production.lot', 'Lot', readonly=True),
        'in_date': fields.datetime('Incoming Date', readonly=True),
        'operation': fields.selection([
                                ('bloque', u'Bloqué'),
                                ('debloque', u'Débloqué'),
                                ('change_location', 'Changement emplacement'),
                                ('rebut', 'Mise au rebut')], 'Operation', readonly=True),     
    }
    
    def init(self, cr):
        tools.drop_view_if_exists(cr, 'report_stock_lot_dest_rebut')
        tools.drop_view_if_exists(cr, 'report_stock_lot_src_rebut')
        tools.drop_view_if_exists(cr, 'report_stock_lot_rebut')
        cr.execute("""
                CREATE OR REPLACE view report_stock_lot_dest_rebut AS (
                SELECT
                        min(move.id) as id,
                        sum(move.product_qty) as qty,
                        move.restrict_lot_id as lot_id,
                        move.product_id as product_id,
                        move.location_dest_id as location_id,
                        max(move.date) as in_date
                FROM
                        stock_move move
                        INNER JOIN stock_location location ON (location.id = move.location_dest_id)
                WHERE   move.restrict_lot_id is not Null
                AND     move.state = 'done'
                AND     location.usage != 'view'
                AND     location.scrap_location = True
                GROUP BY move.restrict_lot_id, move.product_id, move.location_dest_id
                ORDER BY move.product_id
               );
               
               CREATE OR REPLACE view report_stock_lot_src_rebut AS (
                SELECT
                        min(move.id) as id,
                        sum(move.product_qty) as qty,
                        move.restrict_lot_id as lot_id,
                        move.product_id as product_id,
                        move.location_id as location_id,
                        max(move.date) as in_date
                FROM
                        stock_move move
                        INNER JOIN stock_location location ON (location.id = move.location_id)
                WHERE   move.restrict_lot_id is not Null
                AND     move.state = 'done'
                AND     location.usage != 'view'
                AND     location.scrap_location = True
                GROUP BY move.restrict_lot_id, move.product_id, move.location_id
                ORDER BY move.product_id
               );
               
               CREATE OR REPLACE view report_stock_lot_rebut AS (
                SELECT * FROM 
                (SELECT
                        r1.id as id,
                        CASE 
                            WHEN r2.qty is null THEN r1.qty
                            WHEN r2.qty is not null THEN r1.qty - r2.qty
                            ELSE 0
                        END as qty,
                        r1.lot_id as lot_id,
                        r1.product_id as product_id,
                        r1.location_id as location_id,
                        r1.in_date as in_date,
                        'rebut' as operation
                FROM
                        report_stock_lot_dest_rebut r1
                        LEFT JOIN report_stock_lot_src_rebut r2 
                        ON r1.location_id = r2.location_id
                        AND r1.lot_id = r2.lot_id
                        AND r1.product_id = r2.product_id) AS R
                        WHERE R.qty > 0
               )
        """)
    
report_stock_lot_rebut()
