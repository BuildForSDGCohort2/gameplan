# Copyright (c) 2022, Frappe Technologies Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
import gameplan
from frappe.model.document import Document

class TeamDiscussionVisit(Document):
	def after_insert(self):
		gameplan.refetch_resource('UnreadItems', user=self.user)

	def on_change(self):
		if self.has_value_changed('last_visit'):
			gameplan.refetch_resource('UnreadItems', user=self.user)
