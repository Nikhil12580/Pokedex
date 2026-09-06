import tkinter as tk
from tkinter import messagebox
import requests
import random
from io import BytesIO
from PIL import Image, ImageTk

def get_region(pokemon_id):
    if pokemon_id<=151:
        return"Kanto"
    elif pokemon_id<=251:
        return"Johto"
    elif pokemon_id<=386:
        return"Hoenn"
    elif pokemon_id<=493:
        return"Sinnoh"
    elif pokemon_id<=649:
        return"Unova"
    elif pokemon_id<=721:
        return"Kalos"
    elif pokemon_id<=809:
        return"Alola"
    elif pokemon_id<=905:
        return"Galar"
    else:
        return"Paldea"

def add_section(title):
    info_text.insert(tk.END,"\n"+"="*35+"\n")
    info_text.insert(tk.END,f"{title:^35}\n")
    info_text.insert(tk.END,"="*35+"\n")

def find_evolution_paths(chain,target_name,path=None):
    if path is None:
        path=[]
    current_name=chain["species"]["name"]
    current_path=path+[current_name]
    if current_name.lower()==target_name.lower():
        return [current_path]
    paths=[]
    for evolution in chain["evolves_to"]:
        paths.extend(
            find_evolution_paths(
                evolution,
                target_name,
                current_path
            )
        )
    return paths

def show_evolution_chain(chain,target_name):
    paths=find_evolution_paths(chain,target_name)
    if not paths:
        return
    if len(paths)==1 and len(paths[0])==1:
        for evolution in chain["evolves_to"]:
            info_text.insert(
                tk.END,
                f"{chain['species']['name'].title()}->"
                f"{evolution['species']['name'].title()}\n"
            )
    else:
        for path in paths:
            info_text.insert(
                tk.END,
                "->".join(name.title() for name in path)+ "\n"
            )

def show_evolution_requirements(chain, target_name):
    if chain["species"]["name"].lower() == target_name.lower():
        for evolution in chain["evolves_to"]:
            current_name = chain["species"]["name"].title()
            next_name = evolution["species"]["name"].title()

            info_text.insert(
                tk.END,
                f"{current_name}->{next_name}\n"
            )

            for details in evolution["evolution_details"]:
                if details.get("min_level"):
                    info_text.insert(
                        tk.END,
                        f"Requirement:Level {details['min_level']}\n"
                    )
                elif details.get("item"):
                    item_name = (
                        details["item"]["name"]
                        .replace("-", " ")
                        .title()
                    )
                    info_text.insert(
                        tk.END,
                        f"Requirement:{item_name}\n"
                    )
                elif details.get("min_happiness"):
                    info_text.insert(
                        tk.END,
                        f"Requirement: Happiness {details['min_happiness']}\n"
                    )
                elif details.get("location"):
                    location_name = (
                        details["location"]["name"]
                        .replace("-", " ")
                        .title()
                    )
                    info_text.insert(
                        tk.END,
                        f"Requirement:Level up at {location_name}\n"
                    )
                elif details.get("trigger", {}).get("name") == "trade":
                    info_text.insert(
                        tk.END,
                        "Requirement:Trade\n"
                    )

        return
    def find_path(node, target):
        if node["species"]["name"].lower() == target.lower():
            return [node]

        for evolution in node["evolves_to"]:
            result = find_path(evolution, target)
            if result:
                return [node] + result

        return None

    path = find_path(chain, target_name)

    if not path or len(path) < 2:
        return

    for i in range(len(path) - 1):
        current = path[i]
        evolution = path[i + 1]

        current_name = current["species"]["name"].title()
        next_name = evolution["species"]["name"].title()

        info_text.insert(
            tk.END,
            f"{current_name}->{next_name}\n"
        )

        for details in evolution["evolution_details"]:
            if details.get("min_level"):
                info_text.insert(
                    tk.END,
                    f"Requirement:Level {details['min_level']}\n"
                )
            elif details.get("item"):
                item_name = (
                    details["item"]["name"]
                    .replace("-", " ")
                    .title()
                )
                info_text.insert(
                    tk.END,
                    f"Requirement:{item_name}\n"
                )
            elif details.get("min_happiness"):
                info_text.insert(
                    tk.END,
                    f"Requirement: Happiness {details['min_happiness']}\n"
                )
            elif details.get("location"):
                location_name = (
                    details["location"]["name"]
                    .replace("-", " ")
                    .title()
                )
                info_text.insert(
                    tk.END,
                    f"Requirement:Level up at {location_name}\n"
                )
            elif details.get("trigger", {}).get("name") == "trade":
                info_text.insert(
                    tk.END,
                    "Requirement:Trade\n"
                )

current_shiny_url=None
showing_shiny=False
current_sprite_url=None
def show_shiny():
    global current_shiny_url
    if current_shiny_url:
        try:
            image_response=requests.get(current_shiny_url,timeout=10)
            image_response.raise_for_status()
            image=Image.open(BytesIO(image_response.content)).convert("RGBA")
            image=image.resize((180,180),Image.Resampling.NEAREST)
            shiny_image=ImageTk.PhotoImage(image)
            sprite_label.config(image=shiny_image,text="")
            sprite_label.image=shiny_image
        except Exception:
            sprite_label.config(image="",text="No Shiny Sprite")
            
def toggle_shiny():
    global showing_shiny
    if showing_shiny:
        show_normal()
        showing_shiny = False
    else:
        show_shiny()
        showing_shiny = True
        
def show_normal():
    global current_sprite_url
    if current_sprite_url:
        image_response=requests.get(current_sprite_url,timeout=10)
        image_response.raise_for_status()
        image=Image.open(BytesIO(image_response.content)).convert("RGBA")
        image=image.resize((180,180),Image.Resampling.NEAREST)
        normal_image=ImageTk.PhotoImage(image)
        sprite_label.config(image=normal_image,text="")
        sprite_label.image=normal_image

def search_pokemon(search_name=None):
    global current_shiny_url,current_sprite_url,showing_shiny
    if search_name is None:
        name=search_entry.get().strip().lower()
    else:
        name=str(search_name).strip().lower()
    if not name:
        return
    if name.isdigit():
        if int(name)<1 or int(name)>1025:
            messagebox.showerror("Error", "Invalid Pokédex Number")
            return
    if name=="random":
        name=str(random.randint(1,1025))
    try:
        response=requests.get(
            f"https://pokeapi.co/api/v2/pokemon/{name}",
            timeout=10
            )
    except requests.RequestException:
        messagebox.showerror(
            "Error",
            "Pokémon not found. Enter a valid name or Pokédex number."
        )
        return
    data=response.json()
    try:
        species_response=requests.get(
            data["species"]["url"],
            timeout=10
        )
        species_response.raise_for_status()
        species_data=species_response.json()
    except requests.RequestException:
        messagebox.showerror(
            "Error",
            "Could not load Pokémon species data."
        )
        return
    info_text.config(state=tk.NORMAL)
    info_text.delete("1.0",tk.END)
    sprite_url=data["sprites"]["front_default"]
    current_sprite_url=sprite_url
    showing_shiny=False
    current_shiny_url=data["sprites"]["front_shiny"]
    if sprite_url:
        try:
            image_response=requests.get(sprite_url,timeout=10)
            image_response.raise_for_status()
            image=Image.open(
                BytesIO(image_response.content)
            ).convert("RGBA")
            image=image.resize((180,180),Image.Resampling.NEAREST)
            sprite_image=ImageTk.PhotoImage(image)
            sprite_label.config(image=sprite_image, text="")
            sprite_label.image = sprite_image
        except Exception:
            sprite_label.config(image="",text="No Sprite")
            sprite_label.image=None
    else:
        sprite_label.config(image="",text="No Sprite")
        sprite_label.image=None

    pokemon_id=data["id"]
    pokemon_name=data["name"].lower()
    region=get_region(pokemon_id)
    number_label.config(text=f"#{pokemon_id:04d}")
    name_label.config(text=data["name"].title())
    region_label.config(text=f"Region:{region}")

    add_section("CLASSIFICATION")
    category="Unknown"
    for genus_info in species_data["genera"]:
        if genus_info["language"]["name"]=="en":
            category=genus_info["genus"]
            break
    info_text.insert(tk.END,f"category:{category}\n")


    pseudo_legendaries = {
        "dragonite", "tyranitar", "salamence", "metagross",
        "garchomp", "hydreigon", "goodra", "kommo-o",
        "dragapult", "baxcalibur" 
    }

    ultra_beasts = {
        "nihilego", "buzzwole", "pheromosa", "xurkitree",
        "celesteela", "kartana", "guzzlord", "stakataka",
        "blacephalon", "poipole", "naganadel"
    }
    if species_data["is_legendary"]:
        status="🌟 Legendary"
    elif species_data["is_mythical"]:
        status="✨ Mythical"
    elif pokemon_name in pseudo_legendaries:
        status="🔥 Pseudo-Legendary"
    elif pokemon_name in ultra_beasts:
        status="👽 Ultrabeast"
    else:
        status="⚪️ Normal"
    info_text.insert(tk.END,f"Status: {status}\n")

    add_section("TYPES")
    type_icons={
        "normal":"⚪",
        "fire":"🔥",
        "water":"💧",
        "electric":"⚡",
        "grass":"🌿",
        "ice":"❄️",
        "fighting":"🥊",
        "poison":"☠️",
        "ground":"🌍",
        "flying":"🕊️",
        "psychic":"🔮",
        "bug":"🐛",
        "rock":"🪨",
        "ghost":"👻",
        "dragon":"🐉",
        "dark":"🌑",
        "steel":"⚙️",
        "fairy":"🧚",
    }
    for type_info in data["types"]:
        type_name=type_info["type"]["name"]
        icon=type_icons.get(type_name,"?")
        info_text.insert(
            tk.END,
            f"{icon} {type_name.title()}\n"
        )
        
    add_section("ABILITIES")
    for ability_info in data["abilities"]:
        ability_name=(
            ability_info["ability"]["name"]
            .replace("-"," ")
            .title()
        )
        if ability_info["is_hidden"]:
            info_text.insert(
                tk.END,
                f"• {ability_name} (Hidden Ability)\n"
            )
        else:
            info_text.insert(
                tk.END,
                f"• {ability_name}\n"
            )
    
    add_section("PHYSICAL DATA")
    height=data["height"]/10
    weight=data["weight"]/10
    info_text.insert(tk.END,f"Height: {height} m\n")
    info_text.insert(tk.END,f"Weight: {weight} kg\n")
    
    add_section("STATS")
    total_stats=0
    speed=0
    for stat in data["stats"]:
        stat_name=stat["stat"]["name"]
        stat_value=stat["base_stat"]
        total_stats +=stat_value
        if stat_name=="speed":
            speed=stat_value
        info_text.insert(
            tk.END,
            f"{stat_name.title()}: {stat_value}\n"
            )
    info_text.insert(
        tk.END,
        f"Total Stats: {total_stats}\n"
    )
    if total_stats>=600:
        stat_tier="Excellent 🔥"
    elif total_stats>=500:
        stat_tier="Strong 💪"
    elif total_stats>=400:
        stat_tier="Average ⚡"
    else:
        stat_tier="Low 🥲"
    info_text.insert(
        tk.END,
        f"Stat Tier: {stat_tier}\n"
    )
    if speed>=100:
        speed_tier="Fast ⚡"
    elif speed>=60:
        speed_tier="Average 🏃"
    else:
        speed_tier="Slow 🐢"
    info_text.insert(
        tk.END,
        f"Speed Tier: {speed_tier}\n"
    )
    info_text.insert(tk.END, "-------------------\n")

    add_section("GENDER DATA")
    gender_rate=species_data["gender_rate"]
    if gender_rate==-1:
        info_text.insert(tk.END,"Gender: Genderless\n")
    else:
        female=gender_rate*12.5
        male=100-female
        info_text.insert(tk.END, "Gender Ratio\n")
        info_text.insert(tk.END, f"Male: {male}%\n")
        info_text.insert(tk.END, f"Female: {female}%\n")

    add_section("GROWTH / TRAINING DATA")
    growth_rate=(
        species_data["growth_rate"]["name"]
        .replace("-"," ")
        .title()
    )
    info_text.insert(tk.END,f"Growth Rate:{growth_rate}\n")
    info_text.insert(tk.END,f"Base Experience: {data['base_experience']}\n")
    info_text.insert(
        tk.END,
        f"Base Happiness: {species_data['base_happiness']}\n"
    )

    add_section("CATCH DATA")
    info_text.insert(
        tk.END,
        f"Catch Rate: {species_data['capture_rate']}\n"
    )

    add_section("HATCH DATA")
    egg_groups=[]
    for egg_group in species_data["egg_groups"]:
        egg_groups.append(
            egg_group["name"].replace("-", " ").title()
        )
    info_text.insert(
        tk.END,
        f"Egg Groups:{'/'.join(egg_groups)}\n"
    )
    info_text.insert(
        tk.END,
        f"Egg Cycle:{species_data['hatch_counter']}\n"
    )

    add_section("POKÉMON DESCRIPTION")
    description="NO description available."
    for entry in species_data["flavor_text_entries"]:
        if entry["language"]["name"]=="en":
            description=(
                entry["flavor_text"]
                .replace("\n", " ")
                .replace("\f", " ")
            )
            break
    info_text.insert(tk.END, description+"\n")

    add_section("EVOLUTION CHAIN")
    evolution_url=species_data["evolution_chain"]["url"]
    try:
        evolution_response=requests.get(
            evolution_url,
            timeout=10
        )
    except requests.RequestException:
        evolution_response=None
    if evolution_response and evolution_response.status_code==200:
        evolution_data=evolution_response.json()
        show_evolution_chain(evolution_data["chain"],data["name"])

    add_section("EVOLUTION REQUIREMENTS")
    if evolution_response and evolution_response.status_code==200:
        show_evolution_requirements(evolution_data["chain"],data["name"])

    add_section("MOVES")
    for move_info in data["moves"][:20]:
        move_name=(
            move_info["move"]["name"]
            .replace("-"," ")
            .title()
        )
        info_text.insert(tk.END,f"• {move_name}\n")
    info_text.insert(
        tk.END,
        f"Total Moves: {len(data['moves'])}\n"
    )

    add_section("WEAKNESSESS")
    weaknesses={}
    for weakness_info in data["types"]:
        type_url=weakness_info["type"]["url"]
        try:
            type_response=requests.get(
                type_url,
                timeout=10
            )
        except requests.RequestException:
            continue
        if type_response.status_code==200:
            type_data=type_response.json()
            for damage_relation in type_data["damage_relations"]["double_damage_from"]:
                weakness_name=damage_relation["name"]
                if weakness_name in weaknesses:
                    weaknesses[weakness_name]*=2
                else:
                    weaknesses[weakness_name]=2
    for weakness_name,multiplier in weaknesses.items():
        info_text.insert(
            tk.END,
            f"{weakness_name.title()}->{multiplier}x\n"
        )

    add_section("RESISTANCE")
    resistances={}
    for type_info in data["types"]:
        type_url=type_info["type"]["url"]
        try:
            type_response=requests.get(
                type_url,
                timeout=10
            )
        except requests.RequestException:
            continue
        if type_response.status_code==200:
            type_data=type_response.json()
            for relation in type_data["damage_relations"]["half_damage_from"]:
                resistance_name=relation["name"]
                resistances[resistance_name]=0.5
    for resistance_name,multiplier in resistances.items():
        info_text.insert(
            tk.END,f"{resistance_name.title()}->{multiplier}x\n"
        )

    add_section("IMMUNITIES")
    immunities={}
    for type_info in data["types"]:
        type_url=type_info["type"]["url"]
        try:
            type_response=requests.get(
                type_url,
                timeout=10
            )
        except requests.RequestException:
            continue
        if type_response.status_code==200:
            type_data=type_response.json()
            for relation in type_data["damage_relations"]["no_damage_from"]:
                immunity_name=relation["name"]
                immunities[immunity_name]=0
    for immunity_name,multiplier in immunities.items():
        info_text.insert(
            tk.END,
            f"{immunity_name.title()}->{multiplier}x\n"
        )
    info_text.tag_add("center", "1.0", "end")
    info_text.config(state=tk.DISABLED) 

def random_pokemon():
    search_pokemon(random.randint(1,1025))

current_shiny_url=None
root=tk.Tk()
root.title("Pokédex")
root.configure(bg="#D32F2F")
root.geometry("700x760")
root.minsize(600,700)
indicator_frame=tk.Frame(root,bg="#D32F2F")
indicator_frame.pack(fill="x",padx=35,pady=(8,0))
lens=tk.Canvas(
    indicator_frame,
    width=120,
    height=60,
    bg="#D32F2F",
    highlightthickness=0
)
lens.pack(side="left")
lens.create_oval(
    5,5,55,55,
    fill="#00BFFF",
    outline="#B8F3FF",
    width=4
)
lens.create_oval(5,5,55,55,fill="#00BFFF",outline="#B8F3FF",width=4)
lens.create_oval(68,22,78,32,fill="#E53935",outline="")
lens.create_oval(84,22,94,32,fill="#FDD835",outline="")
lens.create_oval(100,22,110,32,fill="#43A047",outline="")
title_frame=tk.Frame(root,bg="#D32F2F")
title_frame.pack(pady=12)
title_label=tk.Label(
    title_frame,
    text="POKÉDEX",
    font=("Arial",26,"bold"),
    bg="#D32F2F"
)
title_label.pack(side="left",padx=(0,15))
pokeball=tk.Canvas(
    title_frame,
    width=55,
    height=55,
    bg="#D32F2F",
    highlightthickness=0
)
pokeball.pack(side="left")
pokeball.create_oval(4,4,51,51,fill="white",outline="black",width=2)
pokeball.create_arc(4,4,51,51,start=0,extent=180,fill="red",outline="black",width=2)
pokeball.create_line(5,27,50,27,fill="black",width=2)
pokeball.create_oval(19,19,36,36,fill="white",outline="black",width=2)
search_frame=tk.Frame(root,bg="#D32F2F")
search_frame.pack(pady=8)
search_entry=tk.Entry(
    search_frame,
    font=("Arial",14),
    width=28
)
search_entry.grid(row=0,column=0,padx=5)
search_button=tk.Button(
    search_frame,
    text="Search Pokémon",
    font=("Arial",11,"bold"),
    width=15,
    command=search_pokemon
)
search_button.grid(row=0,column=1,padx=5)
random_button=tk.Button(
    search_frame,
    text="Random",
    font=("Arial",11,"bold"),
    width=15,
    command=random_pokemon
)
random_button.grid(row=0,column=2,padx=5)
top_frame=tk.Frame(root,bg="#D32F2F")
top_frame.pack(fill="x",padx=30,pady=15)
sprite_label=tk.Label(
    top_frame,
    text="Search a Pokémon",
    font=("Arial",12),
    bg="#D32F2F"
)
sprite_label.pack(side="left",padx=35)
shiny_button=tk.Button(
    top_frame,
    text="✨ Shiny",
    font=("Arial",10,"bold"),
    command=toggle_shiny
)
shiny_button.pack(side="left",padx=5)
basic_frame=tk.Frame(top_frame,bg="#D32F2F")
basic_frame.pack(side="left",padx=25)
number_label=tk.Label(
    basic_frame,
    text="#----",
    font=("Arial",16),
    bg="#D32F2F"
)
number_label.pack(anchor="w")
name_label=tk.Label(
    basic_frame,
    text="Pokémon Name",
    font=("Arial",22,"bold"),
    bg="#D32F2F"
)
name_label.pack(anchor="w",pady=5)
region_label=tk.Label(
    basic_frame,
    text="Region: ---",
    font=("Arial",14),
    bg="#D32F2F"
)
region_label.pack(anchor="w")
text_frame=tk.Frame(root,bg="#F5F5F5",height=400)
text_frame.pack(fill="both",expand=False,padx=20,pady=15)
text_frame.pack_propagate(False)
scrollbar=tk.Scrollbar(text_frame,bg="#1565C0")
scrollbar.pack(side="right",fill="y",padx=(5,0))
info_text=tk.Text(
    text_frame,
    font=("consolas",11),
    wrap="word",
    padx=10,
    pady=10,
    bg="#1565C0",
    fg="white",
    insertbackground="white",
    yscrollcommand=scrollbar.set
)
info_text.tag_configure("center",justify="center")
info_text.pack(side="left",fill="both",expand=True,padx=12,pady=12)
scrollbar.config(command=info_text.yview)
info_text.tag_configure("center", justify="center")
info_text.insert(
    tk.END,
    "Search for a Pokémon to display its complete Pokédex entry."   
)
info_text.tag_add("center", "1.0", "end")
info_text.config(state=tk.DISABLED)
root.bind("<Return>",lambda event:search_pokemon())
root.mainloop()