from dataclasses import dataclass
from pathlib import Path
from string import Template
from typing import Optional

from idgen import generate_handle, generate_guid

OUTPUT_DIR = Path(__file__).parent / 'output'
OUTPUT_XAML = OUTPUT_DIR / 'ppmeter_widget.xaml'
OUTPUT_LOCA = OUTPUT_DIR / 'ppmeter_loca_tech.xml'
OUTPUT_ACTION_RESOURCE_DEFINITIONS = OUTPUT_DIR / 'ppmeter_action_resource_definitions.lsx'

TEMPLATE_ACTION_RESOURCE_DEFINITION = """
                <node id="ActionResourceDefinition">
                    <attribute id="DisplayName" type="TranslatedString" handle="{handle}" version="1"/>
                    <attribute id="Name" type="FixedString" value="{name}"/>
                    <attribute id="ReplenishType" type="FixedString" value="Never"/>
                    <attribute id="ShowOnActionResourcePanel" type="bool" value="false"/>
                    <attribute id="UUID" type="guid" value="{guid}"/>
                </node>"""

TEMPLATE_TRANSLATED_STRING = '<content contentuid="{handle}" version="1">{name}</content>'

# substitute stat_name and float_format (set '' if not needed)
TEMPLATE_WIDGET_VALUES = Template("""
                <DataTemplate x:Key="PPMeter${stat_name}Template">
                    <StackPanel>
                        <ItemsControl x:Name="ActionResourcesList" ItemsSource="{Binding Stats.ActionResources}" HorizontalAlignment="Center" VerticalAlignment="Bottom">
                            <ItemsControl.ItemTemplate>
                                <DataTemplate>
                                    <TextBlock Text="{Binding Value${float_format}}">
                                        <TextBlock.Style>
                                            <Style TargetType="TextBlock">
                                                <Setter Property="Visibility" Value="Collapsed"/>
                                                <Style.Triggers>
                                                    <DataTrigger Binding="{Binding Name, Converter={StaticResource CompareStringConverter}, ConverterParameter='PPMeter${stat_name}'}" Value="True">
                                                        <Setter Property="Visibility" Value="Visible"/>
                                                    </DataTrigger>
                                                </Style.Triggers>
                                            </Style>
                                        </TextBlock.Style>
                                    </TextBlock>
                                </DataTemplate>
                            </ItemsControl.ItemTemplate>
                        </ItemsControl>
                    </StackPanel>
                </DataTemplate>""")

TEMPLATE_WIDGET_TABLE = Template("""
                            <StackPanel Visibility="{Binding IsChecked, ElementName=ToggleHealingTaken, Converter={StaticResource BoolToVisibleConverter}}">
                                <!-- $stat_name Combat -->
                                <ListView ItemsSource="{Binding Data.PartyCharacters}" Visibility="{Binding IsChecked, ElementName=ToggleCombat, Converter={StaticResource BoolToVisibleConverter}}">
                                    <ListView.View>
                                        <GridView>
                                            <GridViewColumn DisplayMemberBinding="{Binding Name}" Header="{Binding Source='h4c07541bg0c4ag4316g95dfgc639cae23097', Converter={StaticResource TranslatedStringConverter}}"/>
                                            <GridViewColumn Header="{Binding Source='h83dc745bg262fg41acg9631g873908251a68', Converter={StaticResource TranslatedStringConverter}}" CellTemplate="{StaticResource PPMeterCombatHealingTakenTemplate}"/>
                                            <GridViewColumn Header="{Binding Source='h3a4ab91agf336g4e20g85bcg4a5a72fad730', Converter={StaticResource TranslatedStringConverter}}" CellTemplate="{StaticResource PPMeterCombatRoundsTemplate}"/>
                                            <GridViewColumn Header="{Binding Source='h5fab9a5eg6bf5g4227g9de1g5e57aad2c88f', Converter={StaticResource TranslatedStringConverter}}" CellTemplate="{StaticResource PPMeterCombatHTPRTemplate}"/>
                                        </GridView>
                                    </ListView.View>
                                </ListView>
                                <!-- $stat_name Day -->
                                <ListView ItemsSource="{Binding Data.PartyCharacters}" Visibility="{Binding IsChecked, ElementName=ToggleDay, Converter={StaticResource BoolToVisibleConverter}}">
                                    <ListView.View>
                                        <GridView>
                                            <GridViewColumn DisplayMemberBinding="{Binding Name}" Header="{Binding Source='h4c07541bg0c4ag4316g95dfgc639cae23097', Converter={StaticResource TranslatedStringConverter}}"/>
                                            <GridViewColumn Header="{Binding Source='h83dc745bg262fg41acg9631g873908251a68', Converter={StaticResource TranslatedStringConverter}}" CellTemplate="{StaticResource PPMeterDayHealingTakenTemplate}"/>
                                            <GridViewColumn Header="{Binding Source='h3a4ab91agf336g4e20g85bcg4a5a72fad730', Converter={StaticResource TranslatedStringConverter}}" CellTemplate="{StaticResource PPMeterDayRoundsTemplate}"/>
                                            <GridViewColumn Header="{Binding Source='h5fab9a5eg6bf5g4227g9de1g5e57aad2c88f', Converter={StaticResource TranslatedStringConverter}}" CellTemplate="{StaticResource PPMeterDayHTPRTemplate}"/>
                                        </GridView>
                                    </ListView.View>
                                </ListView>
                                <!-- $stat_name Level -->
                                <ListView ItemsSource="{Binding Data.PartyCharacters}" Visibility="{Binding IsChecked, ElementName=ToggleLevel, Converter={StaticResource BoolToVisibleConverter}}">
                                    <ListView.View>
                                        <GridView>
                                            <GridViewColumn DisplayMemberBinding="{Binding Name}" Header="{Binding Source='h4c07541bg0c4ag4316g95dfgc639cae23097', Converter={StaticResource TranslatedStringConverter}}"/>
                                            <GridViewColumn Header="{Binding Source='h83dc745bg262fg41acg9631g873908251a68', Converter={StaticResource TranslatedStringConverter}}" CellTemplate="{StaticResource PPMeterLevelHealingTakenTemplate}"/>
                                            <GridViewColumn Header="{Binding Source='h3a4ab91agf336g4e20g85bcg4a5a72fad730', Converter={StaticResource TranslatedStringConverter}}" CellTemplate="{StaticResource PPMeterLevelRoundsTemplate}"/>
                                            <GridViewColumn Header="{Binding Source='h5fab9a5eg6bf5g4227g9de1g5e57aad2c88f', Converter={StaticResource TranslatedStringConverter}}" CellTemplate="{StaticResource PPMeterLevelHTPRTemplate}"/>
                                        </GridView>
                                    </ListView.View>
                                </ListView>
                                <!-- $stat_name Overall -->
                                <ListView ItemsSource="{Binding Data.PartyCharacters}" Visibility="{Binding IsChecked, ElementName=ToggleOverall, Converter={StaticResource BoolToVisibleConverter}}">
                                    <ListView.View>
                                        <GridView>
                                            <GridViewColumn DisplayMemberBinding="{Binding Name}" Header="{Binding Source='h4c07541bg0c4ag4316g95dfgc639cae23097', Converter={StaticResource TranslatedStringConverter}}"/>
                                            <GridViewColumn Header="{Binding Source='h83dc745bg262fg41acg9631g873908251a68', Converter={StaticResource TranslatedStringConverter}}" CellTemplate="{StaticResource PPMeterOverallHealingTakenTemplate}"/>
                                            <GridViewColumn Header="{Binding Source='h3a4ab91agf336g4e20g85bcg4a5a72fad730', Converter={StaticResource TranslatedStringConverter}}" CellTemplate="{StaticResource PPMeterOverallRoundsTemplate}"/>
                                            <GridViewColumn Header="{Binding Source='h5fab9a5eg6bf5g4227g9de1g5e57aad2c88f', Converter={StaticResource TranslatedStringConverter}}" CellTemplate="{StaticResource PPMeterOverallHTPRTemplate}"/>
                                        </GridView>
                                    </ListView.View>
                                </ListView>
                            </StackPanel>""")

LIFETIMES = ('Combat', 'Day', 'Level', 'Overall')


@dataclass
class PPMeterValue:
    name: str
    parent: Optional[str] = None



TABLE_ = [
    PPMeterValue('Rounds'),
    PPMeterValue('Damage'),
]



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


def generate_widget(stat_name: str, float_format=False):
    float_format = ', StringFormat={}{0:F2}' if float_format else ''
    for lifetime in LIFETIMES:
        print(TEMPLATE_WIDGET_VALUES.substitute(stat_name=f'{lifetime}{stat_name}',
                                                float_format=float_format))


if __name__ == '__main__':
    # generate_widget('SHPR', float_format=True)
    generate_action_resource_definitions('SHPR')