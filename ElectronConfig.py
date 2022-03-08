

sub=["s", "s", "p", "s", "p", "s", "d", "p", "s", "d", "p", "s", "f", "d", "p", "s", "f", "d", "p", "f", "d", "f"]
ngas=["[He]", "[Ne]", "[Ar]", "[Kr]", "[Xe]", "[Rn]", "[Og]"]
electron=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
gas_atom=[2,10,18,36,54,86,118]
pquantum=[1,2,2,3,3,4,3,4,5,4,5,6,4,5,6,7,5,6,7,6,7,7]
val=[0,0,0,0,0,0,0]
valShell=[1,2,3,4,5,6,7]
valCharge=[1,2,3,4,-3,-2,-1,0]
elements=["Hydrogen - H",      "Helium - He",        "Lithium - Li",
    "Beryllium - Be",    "Boron - B",          "Carbon - C",
    "Nitrogen - N",      "Oxygen - O",         "Fluorine - F",
    "Neon - Ne",         "Sodium - Na",        "Magnesium - Mg",
    "Aluminum - Al",     "Silicon - Si",       "Phosphorus - P",
    "Sulfur - S",        "Chlorine - Cl",      "Argon - Ar",
    "Potassium - K",     "Calcium - Ca",       "Scandium - Sc",
    "Titanium - Ti",     "Vanadium - V",       "Chromium - Cr",
    "Manganese - Mn",    "Iron - Fe",          "Cobalt - Co",
    "Nickel - Ni",       "Copper - Cu",        "Zinc - Zn",
    "Gallium - Ga",      "Germanium - Ge",     "Arsenic - As",
    "Selenium - Se",     "Bromine - Br",       "Krypton - Kr",
    "Rubidium - Rb",     "Strontium - Sr",     "Yttrium - Y",
    "Zirconium - Zr",    "Niobium - Nb",       "Molybdenum - Mo",
    "Technetium - Tc",   "Ruthenium - Ru",     "Rhodium - Rh",
    "Palladium - Pd",    "Silver - Ag",        "Cadmium - Cd",
    "Indium - In",       "Tin - Sn",           "Antimony - Sb",
    "Tellurium - Te",    "Iodine - I",         "Xenon - Xe",
    "Cesium - Cs",       "Barium - Ba",        "Lanthanum - La",
    "Cerium - Ce",       "Praseodymium - Pr",  "Neodymium - Nd",
    "Promethium - Pm",   "Samarium - Sm",      "Europium - Eu",
    "Gadolinium - Gd",   "Terbium - Tb",       "Dysprosium - Dy",
    "Holmium - Ho",      "Erbium - Er",        "Thulium - Tm",
    "Ytterbium - Yb",    "Lutetium - Lu",      "Hafnium - Hf",
    "Tantalum - Ta",     "Tungsten - W",       "Rhenium - Re",
    "Osmium - Os",       "Iridium - Ir",       "Platinum - Pt",
    "Gold - Au",         "Mercury - Hg",       "Thallium - Tl",
    "Lead - Pb",         "Bismuth - Bi",       "Polonium - Po",
    "Astatine - At",     "Radon - Rn",         "Francium - Fr",
    "Radium - Ra",       "Actinium - Ac",      "Thorium - Th",
    "Protactinium - Pa", "Uranium - U",        "Neptunium - Np",
    "Plutonium - Pu",    "Americium - Am",     "Curium - Cm",
    "Berkelium - Bk",    "Californium - Cf",   "Einsteinium - Es",
    "Fermium - Fm",      "Mendelevium - Md",   "Nobelium - No",
    "Lawrencium - Lr",   "Rutherfordium - Rf", "Dubnium - Db",
    "Seaborgium - Sg",   "Bohrium - Bh",       "Hassium - Hs",
    "Meitnerium - Mt",   "Darmstadtium - Ds",  "Roentgenium - Rg",
    "Copernicium - Cn",  "Nihonium - Nh",      "Flerovium - Fl",
    "Moscovium - Mc",    "Livermorium - Lv",   "Tennessine - Ts",
    "Oganesson - Og"]

def eConfig():
    cur_elec=0
    i=0
    j=0

    #Electron configuration
    while(atom_num!=cur_elec):
        if(sub[i]=="s"):
            cur_elec+=2
            electron[i]+=2
            if(cur_elec>atom_num):
                diff=cur_elec-atom_num
                electron[i]-=diff
                cur_elec=atom_num
        elif(sub[i]=="p"):
            cur_elec+=6
            electron[i]+=6
            if(cur_elec>atom_num):
                diff=cur_elec-atom_num
                electron[i]-=diff
                cur_elec=atom_num
        elif(sub[i]=="d"):
            cur_elec+=10
            electron[i]+=10
            if(cur_elec>atom_num):
                diff=cur_elec-atom_num
                electron[i]-=diff
                cur_elec=atom_num
        elif(sub[i]=="f"):
            cur_elec+=14
            electron[i]+=14
            if(cur_elec>atom_num):
                diff=cur_elec-atom_num
                electron[i]-=diff
                cur_elec=atom_num
        
        i+=1
    
    #Print it
    while(electron[j]!=0):
        print(str(pquantum[j])+sub[j]+str(electron[j]), end=" ")
        j+=1

def nConfig():
    sum=0
    i=0
    j=0

    #Compute
    while(electron[i]!=0):
        sum+=electron[i]
        if(sum>gas_atom[j]):
            j+=1
        i+=1

    sum=0
    i=0

    #Print
    print(ngas[j-1], end=" ")

    while(electron[i]!=0):
        sum+=electron[i]
        if(sum>gas_atom[j-1]):
            print(str(pquantum[i])+sub[i]+str(electron[i]), end=" ")
        i+=1

def atomStruc():
    i=0
    j=0

    while(electron[i]!=0):
        if(pquantum[j]==pquantum[i]):
            val[pquantum[j]-1]+=electron[j]
        i+=1
        j+=1
    
    print("0", end=" ")

    for n in range(7):
        if(val[n]>0):
            print(str(val[n])+")", end=" ")

def valence():
    i=0
    j=0
    group=["Alkali Metals", "Alkaline Earth Metals", "Boron Group", "Carbon Group",
            "Nitrogen Group", "Chalcogen Group", "Halogen Group", "Noble Gas"]
    
    while(i<7 and val[i]!=0):
        i+=1

    print("Valence Shell = "+str(valShell[i-1]))
    print("Valence Electron = "+str(val[i-1]))

    while(valCharge[j]-val[i-1]!=0):
        if(abs(valCharge[j]-val[i-1])==8):
            break
        j+=1
    
    if(valCharge[j]>=1 and valCharge[j]<=3):
        print("Ionic Charge = +"+str(valCharge[j]))
    elif(valCharge[j]==4):
        print("Ionic Charge = +/-"+str(valCharge[j]))
    else:
        print("Ionic Charge = "+str(valCharge[j]))

    print("\nType of element:")

    if(atom_num==1):
        print("Nonmetal")
    elif(atom_num==2):
        print("Noble Gas")
    elif(val[i-1]<4):
        print("Metal")
    elif(val[i-1]==4):
        print("Metal")
    elif(val[i-1]>4 and val[i-1]<8):
        print("Nonmetal")
    else:
        print("Noble Gas")
    
    #Element group name and number
    print("\nElement group:")

    if(val[i-1]>2):
        print(str(group[val[i-1]-1])+" (Group "+str(val[i-1]+10)+")")
    else:
        print(str(group[val[i-1]-1])+" (Group "+str(val[i-1])+")")

def quantums():
    i=0
    j=0
    ml=[-3,-2,-1,0,1,2,3]

    while(electron[i]!=0):
        i+=1
    
    #n
    print("n = "+str(pquantum[i-1]))

    if(sub[i-1]=="s"):
        l=0
        j=1
        start=3
    elif(sub[i-1]=="p"):
        l=1
        j=3
        start=2
    elif(sub[i-1]=="p"):
        l=2
        j=5
        start=1
    else:
        l=3
        j=7
        start=0

    #l
    print("l = "+str(l)+" ("+str(sub[i-1])+")")

    if(electron[i-1]>j):
        charge=abs(electron[i-1]-j)+start
        ms="-1/2"
    else:
        charge=(electron[i-1]-j)+start
        ms="+1/2"

    #ml
    if(ml[charge-1]>0):
        print("ml = +"+str(ml[charge-1]))
    else:
        print("ml = "+str(ml[charge-1]))

    #ms
    print("ms = "+str(ms))

def main():
    global atom_num
    atom_num=int(input("Enter atomic number: "))

    if(atom_num>118):
        print("Invalid element!")
        
main()
print("\nName of Element:\n"+elements[atom_num-1])
print("\nElectron Configuration:")
eConfig()
if(atom_num>2):
    print("\n\nNoble Gas Configuration:")
    nConfig()
print("\n\nAtomic Structure:")
atomStruc()
print("\n\nValence Information:")
valence()
print("\nQuantum Numbers:")
quantums()
