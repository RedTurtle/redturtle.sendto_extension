
def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    
    from AccessControl import ModuleSecurityInfo
    from AccessControl import allow_module, allow_class
    
    allow_module('Products.CMFPlone.utils')
