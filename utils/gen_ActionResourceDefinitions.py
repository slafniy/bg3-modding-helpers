from idgen import generate_handle, generate_guid

TEMPLATE_ACTION_RESOURCE_DEFINITION = """
                <node id="ActionResourceDefinition">
                    <attribute id="DisplayName" type="TranslatedString" handle="{handle}" version="1"/>
                    <attribute id="Name" type="FixedString" value="{name}"/>
                    <attribute id="ReplenishType" type="FixedString" value="Never"/>
                    <attribute id="ShowOnActionResourcePanel" type="bool" value="false"/>
                    <attribute id="UUID" type="guid" value="{guid}"/>
                </node>"""

TEMPLATE_TRANSLATED_STRING = '<content contentuid="{handle}" version="1">{name}</content>'

LIFETIMES = ('Combat', 'Day', 'Level', 'Overall')


def generate_action_resource_definitions(resource_name: str, base_name='PPMeter', lifetimes=LIFETIMES):
    definitions = []
    translations = []
    names = []

    for lifetime in lifetimes:
        names.append(f'{base_name}{lifetime}{resource_name}')

    for name in names:
        handle = generate_handle()
        guid = generate_guid()
        definitions.append(TEMPLATE_ACTION_RESOURCE_DEFINITION[1:].format(handle=handle, name=name, guid=guid))
        translations.append(TEMPLATE_TRANSLATED_STRING.format(handle=handle, name=name))

    [print(d) for d in definitions]
    [print(t) for t in translations]


if __name__ == '__main__':
    generate_action_resource_definitions('Healing')