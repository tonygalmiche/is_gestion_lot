# -*- coding: utf-8 -*-


from datetime import datetime, timedelta
import time
from openerp import pooler
from openerp.osv import fields, osv
from openerp.tools.translate import _

class stock_location(osv.osv):
    _inherit = 'stock.location'
    
    _columns = {
        'control_quality': fields.boolean(u'Contrôle qualité'),
    }
    
stock_location()

class is_commentaire_mouvement_stock(osv.osv):
    _name = 'is.commentaire.mouvement.stock'
    _description = 'Comentaires sur les mouvements'
    
    _columns = {
        'name': fields.char('Description', required=True),
    }
    
is_commentaire_mouvement_stock()