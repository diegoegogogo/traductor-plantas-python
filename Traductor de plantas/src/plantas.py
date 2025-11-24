"""
Generador de Dataset: Plantas con 30 días de lecturas de humedad
Ordenadas alfabéticamente
Basado en el archivo Excel proporcionado
"""

import random
import csv

# Lista COMPLETA de plantas del archivo Excel
plantas = """Aaron's Beard
Absaroka Range Beardtongue
Acacia
Airplant
Alaskan Cup Lichen
Alpine Bittercress
Alpine Buttercup
Alpine Lovage
Alpine Mirrorplant
Alumroot
American Globeflower
Andalusian Pohlia Moss
Andreaea Moss
Angelwing Jasmine
Anglestem Indian Mallow
Anisomeridium Lichen
Annual Checkerbloom
Annual Ragweed
Annual Vetchling
Anthony Peak Lupine
Antifever Fontinalis Moss
Antilles False Holly
Appalachia False Bindweed
Appalachian Clubmoss
Appalachian Stitchwort
Arctic Lupine
Arctoa Moss
Arizona Fescue
Arizona Lescuraea Moss
Arizona Pricklypoppy
Arizona Sandmat
Arizona Snakeweed
Arnold's Parmotrema Lichen
Arrowfeather Threeawn
Arthothelium Lichen
Asian Indigo
Asian White Birch
Aster
Astrothelium Lichen
Australian Amaranth
Austrian Chamomile
Avocado
Aztec Goldenbush
Bachmanniomyces Lichen
Bachman's Jelly Lichen
Ballhead Ipomopsis
Balsamo
Barnacle Lichen
Bartramia Moss
Basswood
Bauhinia
Bay Cedar
Beach Sensitive Pea
Beach Sheoak
Beaked Hazelnut
Beakgrain
Bearded Cinquefoil
Beautiful Sandwort
Bellisima Grande
Bellshape Gilia
Bentflower Milkvetch
Berengena De Paloma
Bitter Cherry
Bitter Root
Black Papillaria Moss
Black River Beardtongue
Black Sand Spikerush
Blair's Wirelettuce
Blind's Bryum Moss
Blue Mountain Milkvetch
Blue Windflower
Blueberry Willow
Bluegreen Saltbush
Bluejoint Panicgrass
Boas' Trematodon Moss
Bog Willowherb
Bolander's Map Lichen
Bolander's Pohlia Moss
Bonnet Orchid
Boreal Fleabane
Brackenfern
Branched Lagophylla
Branched Tearthumb
Brandegee's Buckwheat
Brandegee's Desertparsley
Brasenia
Braun's Erigeron
Brazilian Water Hyacinth
Brazosmint
Bright Green Spikerush
Brilliant Campion
Brittle Sandwort
Britton's Spikerush
Broadleaf Four O'clock
Broomsage
Brown-flower Butterfly Orchid
Bryum Moss
Bulbil Onion
Bulbous Barley
Bulbous Canarygrass
Bushloving Cryptantha
Bushy Heliotrope
Butterbur
Butterfly Milkweed
Butterfly Palm
Cabbagebark Tree
California Bedstraw
California Buckthorn
California Goldenbanner
California Horkelia
California Mock Orange
California Orcutt Grass
California Red Fir
Callaway Milkvetch
Calthaleaf Phacelia
Camasey Terciopelo
Canadian Horseweed
Canadian Ricegrass
Canary Island Geranium
Cancer Bush
Cane Bluestem
Canyon Bird's-foot Trefoil
Canyon Gooseberry
Capberry
Cape Bugle-lily
Cape Jasmine
Caribbean Danafern
Carolina Puccoon
Carolina Springbeauty
Carpet Phlox
Carrotwood
Cartilage Lichen
Cephaelis
Ceylon Gooseberry
Chaenothecopsis Lichen
Chaffhead
Checkerbloom
Chestnut Rush
Chestnuthair Fern
Chihuahuan Pine
Chilean Rabbitsfoot Grass
Chinese-quince
Chinquapin Oak
Chiricahua Adder's-mouth Orchid
Cholla
Cienega Seca Oxytheca
Cinchona Shell Lichen
Ciruelas
Cithara Buckwheat
Clackamas Iris
Clammy Cherry
Clappertonia
Clausena
Cleft Phlox
Clermontia
Climbing Rose
Clokey's Fleabane
Coast Yarrow
Coastal Phyllostegia
Coastal Ragweed
Coastal Tarweed
Cobblestone Milkvetch
Cockleshell Lichen
Coffeetree
Cogongrass
Cohoba Tree
Cole's Hawthorn
Colocasia
Colorado Buckhorn Cholla
Colorado Buckwheat
Colorado Tansyaster
Comb Windmill Grass
Common Bird's-foot
Common Fishhook Cactus
Common Hawkweed
Common Rush
Common St. Paul's Wort
Compton Oak
Confused Astrothelium Lichen
Congdon's False Horkelia
Contorted Pogonatum Moss
Contura Creek Sandmat
Corema
Corn Chamomile
Corynocarpus
Corzo's Wild Petunia
Cotta Grass
Crabseye Lichen
Cracked Lichen
Crater Lichen
Creeping Maiden Fern
Creeping Strawberry Bush
Cresta De Gallo Blanco
Cuban Swallow-wort
Cuckoo Flower
Cumin
Cup Lichen
Curryleaftree
Cusick's Draba
Cutleaf Coneflower
Cutleaf Nightshade
Cyanea
Cycad
Cyme Rose
Cypress Panicgrass
Cyrtandra
Dacrycarpus
Damasonium
Dark Raspberry
Davidson's Phacelia
Deam's Rosinweed
Dehesa Beargrass
Denseflower Cordgrass
Desert Combleaf
Desert Gooseberry
Desert Princesplume
Desert Trumpet
Desert Willow
Devil's Blacksnakeroot
Devilsbit
Devil's-claw
Dewey Sedge
Dicranodontium Moss
Dicranum Moss
Didymodon Moss
Dieffenbachia
Diffuseflower Evening Primrose
Dillenius' Speedwell
Dimorphic Snapdragon
Disc Lichen
Discelium Moss
Disguised St. Johnswort
Ditch Rabbitsfoot Grass
Dock
Dogtooth Violet
Don Quixote's Lace
Dot Lichen
Dotted Hawthorn
Downy Carrionflower
Downy Indian Paintbrush
Downy Mistletoe
Drab Phacelia
Drepanocladus Moss
Duck River Bladderpod
Dunegrass
Dust Lichen
Dwarf Four O'clock
Dwarf Marsh Violet
Dwarf Muellerella Lichen
Dwarf Siberian Pine
Dwarf Stickpea
Dyckia
Early Jewelflower
Early Wattle
Eastern Star Sedge
Eastern Wahoo
Eastwood's Buckwheat
Eclipta
Eggleaf Bristle Fern
Eggleaf Fiddleleaf
Egyptian Riverhemp
Elephantear Pricklypear
Elliott's Bentgrass
Engelmann's Hedgehog Cactus
Engelmann's Milkweed
Entodon Moss
Erect Seaberry
Eschscholtz's Buttercup
European Feather Grass
European Gooseberry
European Milkvetch
European White Birch
Ewan's Larkspur
False Indigo
False Ironwort
Fawnlily
Feather River Stonecrop
Fee's Spleenwort
Fellhanera Lichen
Felt Lichen
Fernleaved Pedicularis
Fetid Goosefoot
Fetid Marigold
Field Pumpkin
Field Sagewort
Filmy Kihifern
Fineflower Gilia
Fir Mistletoe
Fishscale Lichen
Fiveleaf Clover
Flatcrown Buckwheat
Flavopunctelia Lichen
Flor De Pasmo
Florida Alicia
Florida Mudmidget
Fluxweed
Fontanesia
Forchhammeria
Fortune Meadowsweet
Fourpetal St. Johnswort
Fox Grape
Fox Sedge
Foxtail Flatsedge
Foxtail Wheatgrass
Fragrant Bedstraw
Fragrant Bursera
Frankincense
Freckled Milkvetch
Fresno County Bird's Beak
Fringed Grass Of Parnassus
Fringed Sedge
Fringed Spineflower
Fringed Wattle
Fritillary
Front Range Milkvetch
Funck's Wart Lichen
Funston's Saxifrage
Fuscidea Lichen
Gentian
Georgia Bully
Georgia Bulrush
Geyer's Sandmat
Giant Snowdrop
Globe Dodder
Gmelin's Saltbush
Gold Coast Jasmine
Gold-of-pleasure
Gorgojo
Graceful Midsorus Fern
Granular Lichen
Granule Earth Lichen
Grapeleaf Geranium
Gray Gum
Graybark Grape
Gray's Flatsedge
Great Valley Phacelia
Great Yellowcress
Green Comet Milkweed
Green Milkweed
Green Pitcherplant
Greenbright
Grimy Mousetail
Groovestem Indian Plantain
Guinea Bactris
Guinea Guava
Guineagrass
Gypsum Springbeauty
Hairy Crabgrass
Hairy Forked Nailwort
Hairy Gumweed
Hairy Knight's-spur
Hairy Melicgrass
Hairy Sandspurry
Hairy Schiedea
Hairy Sedge
Hairy Signalgrass
Hairy Spinifex
Hairy Spotflower
Hammockherb
Harestail Grass
Harlequin Phacelia
Hartweg's Twinevine
Hastings Oak
Hawthorn
Heermann's Bird's-foot Trefoil
Heller's Rosette Grass
Hen's Eyes
Hepp's Cracked Lichen
Herbst's Sandmat
Herzogiella Moss
Highbush Blueberry
Hilgard's Suncup
Hillebrand's Flatsedge
Hillman's Silverscale
Hinckley's Spreadwing
Hoary Bowlesia
Homomallium Moss
Honohono
Horse-gentian
Houttuynia
Howell's Biscuitroot
Huber's Fleabane
Hudson Bay Sedge
Hulten's Crabseye Lichen
Hybrid Alfalfa
Hybrid Hickory
Hybrid Oak
Hybrid Violet
Hypnum Moss
Hyssopleaf Thoroughwort
Icegrass
Idaho Blue-eyed Grass
Idaho Licorice-root
Indian Shot
Indianbush
Indiangrass
Intoxicating Yam
Ionaspis Lichen
Isachne
Ives' Phacelia
Janusia
Japanese False Bindweed
Japanese Thimbleweed
Japanese Violet
Japanese Zelkova
Jelly Lichen
Jerusalem Salvia
Jeweled Distaff Thistle
Jewelweed
Jointed Alkaligrass
Judd's Grass
Juniper Globemallow
Kaffir-lily
Kalalau Valley Stenogyne
Kamchatka Xanthoparmelia Lichen
Kanaloa
Kawa'u
Kay's Grama
King's Clover
Kings River Buckwheat
Knight's-spur
Knotted Hedgeparsley
Koolau Range Delissea
Kopiko Kea
Kosrae Wild Coffee
Kousa Dogwood
Kraenzlin's Peacock Orchid
Kristinsson's Felt Lichen
Krug's White Morning-glory
Kunth's Smallgrass
Lanai False Lobelia
Lance Pottia Moss
Lanceleaf Grapefern
Lanceleaf Springbeauty
Langlois' Fontinalis Moss
Lapland Poppy
Lapland Rosebay
Lapland Sedge
Largeflower Rushlily
Largeleaf Linden
Larkspurleaf Monkshood
Lasianthaea
Late Purple Aster
Laurel Magnolia
Laurel Oak
Leafless Beaked Lady Orchid
Leafy Reedgrass
Leatherleaf Cyanea
Leatherleaf Eelvine
Leatherweed
Lecania Lichen
Lecidea Lichen
Lecidella Lichen
Lecidoma Lichen
Lemmon's Lupine
Lemmon's Sage
Lemon Beebalm
Lemon-flower Gum
Lemonyellow False Goldenaster
Lespedeza
Lesser Canadian St. Johnswort
Lewiston Cornsalad
Lija
Limestone Goldenrod
Little Deserttrumpet
Little Lovegrass
Little Nipple Cactus
Little River Canyon Onion
Livid Sedge
Lobivia
Loch Lomond Eryngo
Lomagramma
London Planetree
Longstalk Clover
Loroco
Lotononis
Low False Bindweed
Low Spurge
Lozano's False Indianmallow
Lugard's Clover
Luquillo Mountain Holly
Macoun's Wart Lichen
Madagascar Olive
Mancos Shale Packera
Manna Gum
Mannagrass
Manyflower Beardtongue
Manzanita
Marcgravia
Maritime Quillwort
Marsh Grass Of Parnassus
Maui Dubautia
Maui Lobelia
Maui Mirrorplant
Mealy Lichen
Menzies' Tansymustard
Merrit
Mertens' Oxytrope
Metz's Wild Petunia
Mexican Hedgenettle
Mexican Thistle
Mildred's Clarkia
Milkmaids
Mirrorplant
Missouri Ironweed
Moffatt's Beardtongue
Mohihi
Monardella
Monk Orchid
Mono Lupine
Monument Valley Milkvetch
Moran's Manzanita
Morrow's Honeysuckle
Mosquito Bills
Mount Shasta Jacob's-ladder
Mountain Avens
Mountain Azalea
Mountain Monardella
Mountain Moonwort
Mountain Saucerflower
Mountain Woodsorrel
Mud Fiddleleaf
Muhly
Mule Mountain Brickellbush
Munnik Fescue
Mustard
Mycobilimbia Lichen
Mycocalicium Lichen
Na Pali Rockwort
Na'ena'e Pua Melemele
Nail Lichen
Naked Buckwheat
Nannyberry
Narrowleaf Arnica
Narrow-leaf Bottlebrush
Narrowleaf Gentian
Narrowleaf Primrose-willow
Narrowleaf Yellowtops
Narrowpoint Knotweed
Navajo Fleabane
Navel Lichen
Necker's Felt Lichen
Neofuscelia Lichen
Neststraw
New England Blackbutt
New Mexican Groundcherry
New Mexico Milkvetch
New Mexico Raspberry
Nodding Buckwheat
Nodding Stickseed
Northern Biscuitroot
Northern Bugleweed
Northern Jacob's-ladder
Northern Moonwort
Northland Cottonsedge
Notothylas
Nylon Hedgehog Cactus
Oahu Clermontia
Oceanspray
Oemleria
'ohi'a Lehua
Oklahoma Blackberry
Oleander
Olivegreen Calcareous Moss
Olympic Mountain Aster
Oracle Oak
Orange Jessamine
Orange Lichen
Orbea
Oregon Figwort
Oregon Twinpod
Oriental Photinia
Owan's Flatsedge
Pachystachys
Pacific Dewberry
Pacific Dogwood
Pacific Hulsea
Pagumpa Milkvetch
Paiute Cypress
Pakaha
Pale Melicope
Pale Seagrape
Palmer's Mariposa Lily
Palo De Hueso
Papaya
Papyrus
Paradise Apple
Parakeetflower
Pareira
Park Willow
Parmelinopsis
Parmentiera
Parmotrema Lichen
Patterson's Bluegrass
Payette Beardtongue
Payson's Sedge
Pearthorn
Peppervine
Peruvian Peperomia
Pick Me Nots
Piedmont Azalea
Pimpernel
Pine Forest Larkspur
Pinewoods Fingergrass
Pingpong-ball Cactus
Pinguin
Pinnacles Buckwheat
Pinnatifid Shield Lichen
Plains Flatsedge
Plainsman Amaranth
Plateau Cyanea
Pleurochaete Moss
Plum
Plumed Beaksedge
Pogonatum Moss
Poinsettia
Poisonwood
Polargrass
Poodle-dog Bush
Pore Lichen
Poreleaf
Porpidia Lichen
Poverty Brome
Powell's Amaranth
Prairie Pleatleaf
Prenanthella
Prettyface
Prickly Spineflower
Pride-of-rochester
Primrose Monkeyflower
Primrose Peerless
Primrose-willow
Prince Albert's Yew
Prostrate False Pimpernel
Puerto Rico Lacebark
Puffcalyx Gilia
Puffsheath Dropseed
Pumice Alpinegold
Punctelia
Purple Chinese Houses
Purple Milkvetch
Purple Mountain Saxifrage
Purple Rushlily
Purple Woodsorrel
Purpleflower Blacksnakeroot
Purplestem Taro
Purpus' Phacelia
Pyxine Lichen
Quararibea
Quinineweed
Rabbit Ear Rockcress
Racomitrium Moss
Radiate Fingergrass
Radishroot Woodsorrel
Ragged Nettlespurge
Raggedlip Orchid
Rattan
Rattan's Sandmat
Rattlesnake Brome
Raven's Primrose-willow
Rayless Tansyaster
Red Hills Vervain
Red Turtlehead
Redfuzz Saxifrage
Redroot Cryptantha
Resinbush
Resurrection Lily
Reverchon's Rosinweed
Richardson's Pondweed
Rigid Sedge
Rinodina Lichen
Rio Grande Ayenia
Rio Grande Tickseed
Robinson's Onion
Rock Gooseberry
Rockbrake
Rockcress
Rock-loving Sandwort
Rockroot
Rocky Mountain Bluebells
Rolland's Bulrush
Rooting Chainfern
Rose Balm
Rose Meadowsweet
Rose Rockcress
Roseflower Stonecrop
Rosette Lichen
Rothrock's Snakeroot
Roth's Andreaea Moss
Rough Indian Paintbrush
Roughhairy Maiden Fern
Roundleaf Geranium
Roundseed Panicgrass
Rubber Rabbitbrush
Rupturewort
Rush Broom
Rustyleaf Cyanea
Sacramento Waxydogbane
Salmon River Locoweed
Salt Sandspurry
Saltbush
San Bernardino Spineflower
San Clemente Island Brodiaea
San Clemente Island Triteleia
San Diego Goldenstar
San Gabriel Mountains Liveforever
San Luis Lupine
Sand Buckwheat
Sandmat
Sandy Field Hairsedge
Santa Rita Mountain Draba
Sarcographa Lichen
Sarita Rosette Grass
Saussurea
Sawsepal Penstemon
Scaled Cloak Fern
Scarlet Firethorn
Schmoll's Milkvetch
Scottish Licorice-root
Scratchbush
Seaheath
Secund Jewelflower
Sego Lily
Senna
Sentry Milkvetch
Serpent Fern
Setchell's Willow
Shadscale Saltbush
Shaggy Fleabane
Sharp's Club Lichen
Shell Lichen
Shellbark Hickory
Shepherd's Purse
Sherman Hoyt Woolstar
Shortleaf Bruchia Moss
Short-lobe Indian Paintbrush
Short's Aster
Shortspur Seablush
Showy Fanpetals
Showy Goldenrod
Shrubland Dubautia
Shy Wallflower
Siberian Currant
Sicklegrass
Sicklepod
Sierra Snapdragon
Silk-floss Tree
Silky Prairie Clover
Silkybent
Silverback
Silverhair Mousetail
Silvery Lupine
Sitka Starwort
Slender Buckwheat
Slender Clubmoss
Slender Hawkweed
Slender Seapurslane
Slender Wheatgrass
Slender Woodland Sedge
Slenderfruit Nutrush
Slimflower Scurfpea
Slimleaf Bur Ragweed
Slimleaf Pawpaw
Small Indian Breadroot
Small Limestone Moss
Small Prescott Orchid
Smallflower Baby Blue Eyes
Smallflower Indian Paintbrush
Smallflowered Milkvetch
Small's Purslane
Small's Yelloweyed Grass
Smith's Draba
Smooth Blackberry
Smooth Cliffbrake
Smooth Four O'clock
Smooth Melanelia Lichen
Smooth Tofieldia
Snake Canyon Milkvetch
Sneed's Pincushion Cactus
Snow Arnica
Sonoran Silverbush
Soot Lichen
Southern Balsampear
Southern Beeblossom
Southern Bog Clubmoss
Spanish Cherry
Sphagnum
Sphinctrina Lichen
Spicebush
Spike Fescue
Spiny Fameflower
Spiral Flag
Spleenwort
Spotted Sandmat
Springbeauty
Sprucemont Flax
Spurry
Spurry Buckwheat
St. Andrew's Cross
Stalked Popcornflower
Starleaf Begonia
Stebbins' False Bindweed
Steele's Eupatorium
Steinia Lichen
Stemless Thistle
Sticky Buckwheat
Stiff Goldenrod
Stiff Sedge
Stinkingtoe
Strapfern
Strawberry Cactus
Streambank Bird's-foot Trefoil
Striped Toadflax
Subalpine Eyebright
Subterranean Vetch
Suksdorf's Desertparsley
Sulphur-flower Buckwheat
Swamp Chestnut Oak
Swamp Justiceweed
Swamp Wedgescale
Sweet Acacia
Syagrus
Syzygium
Tall Oatgrass
Tall Thimbleweed
Tape Dwarf Polypody
Tecate Tarweed
Telfairia
Texan Canoparmelia Lichen
Texas Dutchman's Pipe
Texas Pipewort
Texas Ringstem
Texas Signalgrass
Textile Onion
Thelocarpon Lichen
Thelopsis Lichen
Thermutis Lichen
Thinstem Lady's Mantle
Thread Lichen
Three-lobe Violet
Threenerve Fleabane
Threetip Sagebrush
Thurber's Muhly
Thymeleaf Bluet
Tiburon Jewelflower
Tiger's Claw
Timothy
Tongueshape Bogmat
Toothleaf Goldeneye
Toringo Crab
Tortula Moss
Trans-pecos Indian Paintbrush
Treadsoftly
Tree Blackberry
Treedaisy
Tricharia Lichen
Tripterocladium Moss
Triteleia
Triticale
Tropical Burnweed
Tropical Govenia
Tropical Milkwort
Tropical Nutrush
True Indigo
Tuckerman's Earth Lichen
Tucson Bur Ragweed
Tufted Yellow Woodsorrel
Turpentine Bush
Tushar Mountain Draba
Tusilla
Twinflower
Twistedstalk
Tylothallia Lichen
Uluhe
Umbel Clerodendrum
Umbrellaleaf
Urban's Lineleaf Fern
Utah Agave
Valley Violet
Variableleaf Heartleaf
Veiny Pea
Veiny Pepperweed
Velvetplant
Victorin's Manzanita
Violet Snapdragon
Virginia Lecidea Lichen
Wahiawa Bog Dubautia
Wahiawa Dubautia
Walker's Necklace Fern
Wand Buckwheat
Warm Springs Hawthorn
Wart Lichen
Water Paspalum
Water Wattle
Watermelon
Waterparsnip
Water-trumpet
Waxyleaf Meadow-rue
Weak Sedge
Weber's Saw-wort
Wedgeleaf
Weeping Willow
Weigel's Bryum Moss
West Indian Tonguefern
West Indies Sandmat
Western Brackenfern
Western Bugbane
Western Daisy
Western Mountain Ash
Western Singlespike Sedge
Western Sunflower
Western Tansymustard
Wheel Milkweed
Wheeler's Bluegrass
White Arctic Mountain Heather
White Bladderflower
White Goldenrod
White Kauai Rosemallow
White Moho
White Panicle Aster
White Sagebrush
White Snakeroot
White Thoroughwort
White Twinevine
Whitehair Rosette Grass
Whitetassels
Whitetop
Whitetop Aster
Whorled Yellow Loosestrife
Wilcox's Nipple Cactus
Wild Banyantree
Wild Chives
Wild Comfrey
Wild Sweetwilliam
Wilhelmsia
Winterfat
Wood Reedgrass
Wood Wakerobin
Woodbine
Woodhouse's Bahia
Woodland Calamint
Woodland Wild Coffee
Wool Grass
Woolly Princesplume
Wooton's Holdback
World Map Lichen
Wreath Lichen
Wright's False Mallow
Wright's Rosette Grass
Wrinkleleaf Goldenrod
Yellow Avalanche-lily
Yellow Butterwort
Yellow Jacob's-ladder
Yellow Pond-lily
Yellow-top Mallee-ash
Yellowwhite Cryptantha
Yenisei River Pondweed
Yerba De Cabra
Yerba De Jicotea
Yew Plum Pine""".strip().split('\n')

# Ordenar alfabéticamente y eliminar duplicados
plantas_ordenadas = sorted(set(plantas))

print(f"="*100)
print(f"GENERADOR DE DATASET: PLANTAS CON 30 DÍAS DE LECTURAS DE HUMEDAD")
print(f"="*100)
print(f"\nTotal de plantas: {len(plantas_ordenadas)}")
print(f"Días por planta: 30")
print(f"Total de lecturas: {len(plantas_ordenadas) * 30:,}\n")

def generar_lecturas_humedad(planta_nombre):
    """Genera 30 días de lecturas de humedad para una planta"""
    # Determinar rango según tipo
    nombre_lower = planta_nombre.lower()
    
    if any(word in nombre_lower for word in ['cactus', 'desert', 'succulent', 'cholla']):
        humedad_base = random.uniform(20, 35)
    elif any(word in nombre_lower for word in ['fern', 'moss', 'lichen']):
        humedad_base = random.uniform(60, 80)
    elif any(word in nombre_lower for word in ['water', 'aquatic', 'hyacinth', 'papyrus']):
        humedad_base = random.uniform(70, 85)
    else:
        humedad_base = random.uniform(40, 65)
    
    # Generar 30 días con variación gaussiana
    lecturas = []
    for _ in range(30):
        variacion = random.gauss(0, 3)
        humedad = round(max(10, min(90, humedad_base + variacion)), 2)
        lecturas.append(humedad)
    
    return lecturas

# Generar archivo TXT
print("Generando archivo TXT...")
with open('plantas_humedad_30dias.txt', 'w', encoding='utf-8') as f:
    f.write("="*100 + "\n")
    f.write("DATASET: PLANTAS CON 30 DÍAS DE LECTURAS DE HUMEDAD (ORDENADAS ALFABÉTICAMENTE)\n")
    f.write("="*100 + "\n")
    f.write(f"Total de plantas: {len(plantas_ordenadas)}\n")
    f.write(f"Días por planta: 30\n")
    f.write(f"Formato: [Número]. Nombre de Planta | Día1, Día2, ..., Día30 (% humedad)\n")
    f.write("="*100 + "\n\n")
    
    for i, planta in enumerate(plantas_ordenadas, 1):
        lecturas = generar_lecturas_humedad(planta)
        lecturas_str = ", ".join([f"{h:.2f}" for h in lecturas])
        f.write(f"{i:4d}. {planta:<50s} | {lecturas_str}\n")

print(f"✅ Archivo TXT generado: plantas_humedad_30dias.txt")

# Generar archivo CSV
print("Generando archivo CSV...")
with open('plantas_humedad_30dias.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    
    # Encabezados
    headers = ['Planta'] + [f'Día_{i}' for i in range(1, 31)]
    writer.writerow(headers)
    
    # Datos
    for planta in plantas_ordenadas:
        lecturas = generar_lecturas_humedad(planta)
        fila = [planta] + lecturas
        writer.writerow(fila)

print(f"✅ Archivo CSV generado: plantas_humedad_30dias.csv")

# Mostrar vista previa de las primeras 5 plantas
print(f"\n{'='*100}")
print("VISTA PREVIA - PRIMERAS 5 PLANTAS:")
print(f"{'='*100}\n")

for i, planta in enumerate(plantas_ordenadas[:5], 1):
    lecturas = generar_lecturas_humedad(planta)
    lecturas_str = ", ".join([f"{h:.2f}" for h in lecturas[:10]])  # Solo primeros 10 días
    print(f"{i}. {planta}")
    print(f"   Primeros 10 días: {lecturas_str}... (+ 20 días más)")
    print()

print(f"{'='*100}")
print("PROCESO COMPLETADO EXITOSAMENTE")
print(f"{'='*100}")
print(f"\n📊 Resumen:")
print(f"   • Total de plantas: {len(plantas_ordenadas)}")
print(f"   • Días por planta: 30")
print(f"   • Total de lecturas generadas: {len(plantas_ordenadas) * 30:,}")
print(f"   • Archivos creados:")
print(f"     - plantas_humedad_30dias.txt (formato legible)")
print(f"     - plantas_humedad_30dias.csv (para Excel/análisis)")
print(f"\n✅ Los archivos están listos para usar!")
print(f"{'='*100}\n")