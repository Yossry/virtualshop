
{
    'name': 'Purchase Report by Vendors',
    'version': '13.0.0.0.1',
    'summary': 'Generate purchase report filter by date, vendors, State/status. You can easily generate specific verdor report',
    "description": """
        Vendors wise purchase report,
        purchase report by vendors,
        Purchase report,
        purchase order report,
        purchase report vendors,
        Date to date purchase report,
        
    """,
    'author': 'Kamrul Hasan',
    'maintainer': 'Kamrul Hasan',
    'Company': 'Tech Analyzers',
    'website': 'http://kamrul.net',
    'depends': ['base','contacts','purchase'],
    'license': 'LGPL-3',
    'category': 'Purchase',
    'data':[
        'wizards/purchase_report_wizard.xml',
        'reports/purchase_report_vendor.xml',
        'reports/purchase_reports.xml',
       ],
    'images': ['static/description/banner.png'],
    'price': 0.0,
    'currency': 'EUR',
    'installable': True,
    'auto_install': False,
    'application': True,
    'sequence': 6,
}
