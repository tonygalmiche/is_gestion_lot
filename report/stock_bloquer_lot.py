# -*- coding: utf-8 -*-

from openerp import tools
from openerp.osv import fields,osv
from openerp.addons.decimal_precision import decimal_precision as dp

class report_stock_lot_bloque(osv.osv):
    _name = "report.stock.lot.bloque"
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
        tools.drop_view_if_exists(cr, 'report_stock_lot_bloque')
        cr.execute("""
                CREATE OR REPLACE view report_stock_lot_bloque AS (
                SELECT
                        min(quant.id) as id,
                        sum(quant.qty) as qty,
                        quant.lot_id as lot_id,
                        quant.product_id as product_id,
                        quant.location_id as location_id,
                        'bloque' as operation,
                        max(quant.in_date) as in_date
                FROM
                        stock_quant quant
                        INNER JOIN stock_location location ON (quant.location_id = location.id)
                WHERE   quant.lot_id is not Null
                AND     location.control_quality = False
                AND     location.usage = 'internal'
                GROUP BY quant.lot_id, quant.product_id, quant.location_id
                HAVING     sum(quant.qty) > 0
                ORDER BY quant.product_id
               )
        """)
    
report_stock_lot_bloque()
