#    Author: Leonardo Pistone
#    Copyright 2014 Camptocamp SA
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
import time
from openerp.tests.common import TransactionCase
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as D_FMT


class TestIsSourced(TransactionCase):

    def test_warehouse_dispatch_is_always_sourced(self):
        self.source.procurement_method = 'wh_dispatch'
        self.assertIs(True, self.source._is_sourced())

    def setUp(self):
        super(TestIsSourced, self).setUp()
        LR = self.env['logistic.requisition']
        LRL = self.env['logistic.requisition.line']
        Source = self.env['logistic.requisition.source']
        ModelData = self.env['ir.model.data']

        lr = LR.create({
            'pricelist_id': ModelData.xmlid_to_res_id('product.list0'),
            'partner_id': ModelData.xmlid_to_res_id('base.res_partner_1'),
            'date_delivery': time.strftime(D_FMT),
        })
        lrl = LRL.create({
            'description': '/',
            'requisition_id': lr.id,
            'requested_uom_id': ModelData.xmlid_to_res_id(
                'product.product_uom_unit'),
            'date_delivery': time.strftime(D_FMT),
        })
        self.source = Source.create({
            'requisition_line_id': lrl.id,
        })
