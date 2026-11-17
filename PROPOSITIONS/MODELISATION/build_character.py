"""Original stylized character, with separate editable face and clothing parts."""
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from build_studies import L, box, setup, show


def mesh(name, col, vertices, faces, material, subdivision=0):
    data = bpy.data.meshes.new(name)
    data.from_pydata(vertices, [], faces)
    data.update()
    ob = bpy.data.objects.new(name, data)
    col.objects.link(ob)
    data.materials.append(material)
    for p in data.polygons:
        p.use_smooth = True
    if subdivision:
        mod = ob.modifiers.new("Subdivision", "SUBSURF")
        mod.levels = mod.render_levels = subdivision
    return ob


def loft(name, col, sections, material, sides=40, subdiv=2):
    verts = []
    for i, (center, width, depth) in enumerate(sections):
        c = Vector(center)
        t = Vector(sections[min(i+1,len(sections)-1)][0]) - Vector(sections[max(i-1,0)][0])
        t.normalize()
        u = Vector((0,1,0)).cross(t).normalized()
        v = t.cross(u)
        for j in range(sides):
            a = math.tau*j/sides
            verts.append(c + width*math.cos(a)*u + depth*math.sin(a)*v)
    faces = []
    for i in range(len(sections)-1):
        for j in range(sides):
            k=(j+1)%sides
            faces.append((i*sides+j,i*sides+k,(i+1)*sides+k,(i+1)*sides+j))
    faces += [tuple(reversed(range(sides))),tuple(range(len(verts)-sides,len(verts)))]
    return mesh(name,col,verts,faces,material,subdiv)


def egg(name,col,loc,scale,mat):
    ob=L.sphere(name,col,mat,location=loc)
    ob.scale=scale
    return ob


def line(name,col,points,radius,mat):
    data=bpy.data.curves.new(name,"CURVE")
    data.dimensions="3D"
    data.resolution_u=18
    data.bevel_depth=radius
    data.use_fill_caps=True
    data.bevel_resolution=4
    spline=data.splines.new("BEZIER")
    spline.bezier_points.add(len(points)-1)
    for p,item in zip(spline.bezier_points,points):
        if len(item)==4:
            p.co=item[:3]
            p.radius=item[3]
        else:
            p.co=item
        p.handle_left_type=p.handle_right_type="AUTO"
    ob=bpy.data.objects.new(name,data)
    col.objects.link(ob)
    data.materials.append(mat)
    return ob


def shape(name, col, levels, mat):
    return loft(name,col,[((x,y,z),w,d) for z,x,y,w,d in levels],mat)


def build(continuous=False):
    asset,studio=setup("NORA · Technicienne de terrain")
    face=L.collection("01 · Visage",asset)
    hair=L.collection("02 · Coiffure",asset)
    body=L.collection("03 · Vêtements",asset)
    hands=L.collection("04 · Gants et chaussures",asset)
    trim=L.collection("05 · Surpiqûres et accessoires",asset)
    skin=L.material("Peau · terre rosée",(0.50,0.235,0.145),0.49)
    inner=L.material("Oreille et lèvres",(0.31,0.099,0.072),0.56)
    upper=L.material("Lèvre terre cuite",(0.37,0.118,0.093),0.50)
    lower=L.material("Lèvre basse",(0.49,0.193,0.152),0.48)
    dark=L.material("Brun ombre",(0.058,0.018,0.014),0.56)
    hairmat=L.material("Cheveux châtain sombre",(0.080,0.033,0.022),0.46)
    hairstreak=L.material("Mèches auburn",(0.147,0.052,0.026),0.46)
    glints=L.material("Reflet de mèche",(0.24,0.100,0.058),0.53)
    white=L.material("Sclérotique ivoire",(0.84,0.79,0.69),0.29)
    iris=L.material("Iris vert mousse",(0.105,0.265,0.201),0.30)
    pupil=L.material("Pupille",(0.007,0.010,0.012),0.22)
    stitch=L.material("Toile crème",(0.71,0.55,0.35),0.66)
    jacket=L.material("Toile ocre",(0.61,0.245,0.064),0.62)
    ochre=L.material("Coutures ocre sombre",(0.32,0.105,0.027),0.61)
    teal=L.material("Pantalon pétrole",(0.047,0.165,0.176),0.73)
    tealshade=L.material("Renforts pétrole",(0.023,0.080,0.090),0.68)
    sock=L.material("Caoutchouc et gants",(0.061,0.050,0.045),0.65)
    buck=L.material("Quincaillerie",(0.36,0.405,0.397),0.30,0.65)

    # A continuous head: the jaw, cheeks, orbit and nose live in the same surface.
    rings=[
        (4.98,.10,.17,.16),(5.06,.28,.25,.20),(5.16,.43,.36,.23),(5.28,.54,.43,.25),
        (5.41,.62,.45,.27),(5.54,.69,.46,.30),(5.67,.74,.48,.33),(5.81,.76,.49,.35),
        (5.96,.77,.48,.37),(6.10,.77,.49,.40),(6.24,.75,.51,.41),(6.37,.71,.50,.41),
        (6.50,.64,.46,.38),(6.60,.54,.40,.34),(6.69,.37,.29,.25),(6.75,.08,.10,.07)
    ]
    if continuous:
        # Continuous longitudinal sections from the base of the neck to the cranium.
        # On the transition rings, raise the front beneath the chin while the back
        # stays low at the nape. This makes the under-jaw turn instead of welding
        # two intersecting shells along a visible circular line.
        rings = [
            (4.27,.355,.285,.295),(4.41,.331,.281,.287),(4.55,.310,.272,.279),
            (4.70,.286,.263,.274),(4.83,.283,.255,.279),(4.94,.303,.277,.283),
            (5.015,.336,.306,.289),(5.08,.376,.339,.300),
        ] + [ring for ring in rings if ring[0] >= 5.16]
    verts=[]; faces=[]; steps=96
    def gauss(x,z,cx,cz,sx,sz):
        return math.exp(-((x-cx)/sx)**2-((z-cz)/sz)**2)
    for z,w,f,b in rings:
        for k in range(steps):
            a=math.tau*k/steps
            x=w*math.cos(a)
            front=max(0,-math.sin(a))
            y=0.045 + ((-f*front**.54) if front else b*math.sin(a))
            if front:
                cheeks=sum(gauss(x,z,s*.43,5.65,.23,.17) for s in (-1,1))
                orbit=sum(gauss(x,z,s*.307,5.925,.19,.14) for s in (-1,1))
                nose=.20*gauss(x,z,0,5.73,.155,.135)+.115*gauss(x,z,0,5.90,.102,.24)
                alae=.060*sum(gauss(x,z,s*.105,5.67,.072,.069) for s in (-1,1))
                chin=.064*gauss(x,z,0,5.25,.31,.12)
                mouth=.061*gauss(x,z,0,5.44,.29,.15)
                y+=front**3*(.034*orbit-.067*cheeks-nose-alae-chin-mouth)
            profile_z=z
            if continuous and z<5.36:
                weight=math.exp(-((z-4.99)/.22)**2)
                profile_z += .095*front*front*weight
                profile_z -= .043*max(0,math.sin(a))**2*weight
                y += .022*max(0,math.sin(a))*weight
            verts.append((x,y,profile_z))
    for i in range(len(rings)-1):
        for k in range(steps):
            j=(k+1)%steps
            faces.append((i*steps+k,i*steps+j,(i+1)*steps+j,(i+1)*steps+k))
    faces.extend([tuple(reversed(range(steps))),tuple(range(len(verts)-steps,len(verts)))])
    head_name="GEO_Tete_Cou_Continu" if continuous else "Visage · crâne, mâchoire et nez"
    mesh(head_name,face,verts,faces,skin,2)

    # Eyes are partly inside the skull. Sculpted rims define almond-shaped apertures.
    for s in (-1,1):
        label="G" if s<0 else "D"
        cx=s*.317
        def eye(points):
            return [(cx+s*x,y,z,r) for x,y,z,r in points]

        # The visible sclera follows the same aperture as the lid margins.
        # UV coordinates keep the iris readable without a floating lens.
        eye_mat=white.copy()
        eye_mat.name="Œil · iris et pupille "+label
        nt=eye_mat.node_tree
        bsdf=next(n for n in nt.nodes if n.type=="BSDF_PRINCIPLED")
        uv=nt.nodes.new("ShaderNodeTexCoord")
        distance=nt.nodes.new("ShaderNodeVectorMath")
        distance.operation="DISTANCE"
        distance.inputs[1].default_value=(.51,.51,0)
        nt.links.new(uv.outputs["UV"],distance.inputs[0])
        ramp=nt.nodes.new("ShaderNodeValToRGB")
        nt.links.new(distance.outputs["Value"],ramp.inputs["Fac"])
        stops=[(.0,(.007,.012,.014,1)),(.094,(.007,.012,.014,1)),
               (.108,(.065,.23,.17,1)),(.168,(.135,.34,.24,1)),
               (.182,(.026,.066,.054,1)),(.191,(.73,.68,.58,1)),
               (.50,(.88,.83,.74,1))]
        cr=ramp.color_ramp
        cr.elements.remove(cr.elements[1])
        for i,(position,color) in enumerate(stops):
            elem=cr.elements[0] if i==0 else cr.elements.new(position)
            elem.position=position
            elem.color=color
        nt.links.new(ramp.outputs["Color"],bsdf.inputs["Base Color"])

        def opening(u,v):
            x=.194*u
            rounded=max(0,1-u*u)**.64
            mid=5.925+.019*u
            z=mid+(v*(.091 if v>=0 else .079))*rounded
            y=-.532+.113*(abs(u)**1.65)+.024*v*v*rounded+.008*u
            return (cx+s*x,y,z)

        ev=[]; ef=[]; eu=[]
        across=48; rows=20
        for j in range(rows+1):
            v=2*j/rows-1
            for k in range(across+1):
                u=1.998*k/across-.999
                x,y,z=opening(u,v)
                ev.append((x,y,z))
                eu.append((.5+(x-cx)/.48,.5+(z-5.925)/.48))
        for j in range(rows):
            for k in range(across):
                h=j*(across+1)+k
                poly=(h,h+1,h+across+2,h+across+1)
                ef.append(poly if s>0 else tuple(reversed(poly)))
        aperture=mesh("Surface visible de l’œil "+label,face,ev,ef,eye_mat)
        layer=aperture.data.uv_layers.new(name="Aperture")
        for loop in aperture.data.loops:
            layer.data[loop.index].uv=eu[loop.vertex_index]

        for v,part,radius in ((1,"Paupière haute",.041),(-1,"Paupière basse",.034)):
            border=[]
            for u in (-1,-.78,-.50,-.20,.12,.44,.73,1):
                x,y,z=opening(u,v)
                border.append((x,y+.002,z,.46+.55*(1-u*u)))
            line(part+" "+label,face,border,radius,skin)
        liner=[]
        for u in (-.985,-.72,-.4,0,.4,.73,.98):
            x,y,z=opening(u,1)
            liner.append((x,y-.017,z-.007,.28+.74*(1-u*u)))
        line("Bord de paupière "+label,face,liner,.012,dark)
        line("Sourcil "+label,face,eye([(-.169,-.452,6.152,.60),(-.075,-.459,6.208,1.18),(.041,-.444,6.232,1.03),(.140,-.403,6.205,.76),(.199,-.365,6.159,.25)]),.046,hairmat)
        ear=egg("Oreille "+label,face,(s*.723,-.015,5.690),(.138,.130,.231),skin)
        ear.rotation_euler.y=s*.20
        egg("Conque "+label,face,(s*.760,-.124,5.697),(.070,.012,.129),inner)
        line("Hélix "+label,face,[(s*.759,-.131,5.549,.5),(s*.822,-.111,5.640,1),(s*.824,-.098,5.765,1),(s*.765,-.109,5.846,.55)],.026,skin)
        egg("Ombre narine "+label,face,(s*.085,-.595,5.647),(.029,.009,.013),inner)
        egg("Clou d’oreille "+label,trim,(s*.771,-.131,5.532),(.028,.019,.028),buck)
    line("Lèvre supérieure",face,[(-.274,-.443,5.446,.3),(-.166,-.488,5.459,.74),(-.078,-.514,5.476,1),(0,-.521,5.462,.76),(.082,-.514,5.477,.97),(.175,-.488,5.460,.7),(.270,-.451,5.454,.23)],.031,upper)
    line("Lèvre inférieure",face,[(-.255,-.450,5.436,.18),(-.151,-.501,5.416,.73),(0,-.526,5.410,1),(.153,-.503,5.424,.71),(.265,-.453,5.451,.17)],.037,lower)
    line("Commissures et bouche",face,[(-.272,-.459,5.447,.25),(-.159,-.520,5.441,.74),(0,-.553,5.446,.8),(.151,-.522,5.448,.70),(.272,-.460,5.455,.25)],.012,dark)

    # Hair cap along a deliberate hairline, plus broad swept locks.
    hv=[]; hf=[]
    for i in range(17):
        t=i/16
        for k in range(96):
            a=math.tau*k/96; sf=math.sin(a)
            end=(1.17+.29*abs(math.cos(a))) if sf<0 else (1.89-.09*abs(math.cos(a)))
            p=.015 + t*end
            hv.append((-.025+.836*math.sin(p)*math.cos(a), .115+.60*math.sin(p)*sf,6.075+.86*math.cos(p)))
    for i in range(16):
        for k in range(96):
            q=(k+1)%96
            hf.append((i*96+k,(i+1)*96+k,(i+1)*96+q,i*96+q))
    hf.append(tuple(range(96)))
    cap=mesh("Implantation et coiffe",hair,hv,hf,hairmat,1)
    mod=cap.modifiers.new("Épaisseur de la coiffe","SOLIDIFY"); mod.thickness=.036
    for i in range(6):
        a=i/5
        points=[((.55-.095*i),-.229+.014*i,6.64+.024*i,.38),
                ((.275-.095*i),-.432+.007*i,6.80+.021*i,1.07),
                ((-.16-.073*i),-.539+.011*i,6.745+.020*i,1.24),
                ((-.48-.028*i),-.564+.025*i,6.57+.043*i,.85),
                ((-.668-.013*i),-.409+.033*i,6.29+.052*i,.11)]
        line("Mèche balayée %02d"%i,hair,points,.105,hairstreak if i in (1,4) else hairmat)
    for s in (-1,1):
        line("Patte",hair,[(s*.690,-.278,6.50,.8),(s*.766,-.245,6.30,1),(s*.762,-.20,6.10,.88),(s*.72,-.094,5.81,.20)],.112,hairmat)
    line("Mèche fine",hair,[(.17,-.465,6.89,.20),(-.15,-.565,6.86,.9),(-.46,-.596,6.72,.81),(-.65,-.519,6.51,.13)],.032,glints)
    egg("Chignon",hair,(.025,.522,6.38),(.43,.38,.43),hairmat)
    line("Attache",hair,[(-.285,.52,6.33,.50),(-.185,.793,6.36,1),(.10,.879,6.36,1),(.305,.715,6.33,.50)],.05,jacket)

    # Clothed figure, kept in distinct, overlapping garment volumes.
    if not continuous:
        shape("Cou",face,[(4.30,0,.06,.34,.26),(4.49,0,.04,.33,.27),(4.72,0,.04,.292,.262),
        (4.91,0,.07,.283,.265),(5.08,0,.08,.278,.260),(5.24,0,.10,.24,.239)],skin)
    shape("Veste · épaules et bassin",body,[(2.77,0,.045,.63,.37),(2.90,0,.04,.74,.43),(3.20,0,.04,.70,.39),(3.55,0,.03,.72,.43),(3.93,0,.04,.86,.48),(4.25,0,.05,.92,.43),(4.46,0,.05,.68,.35),(4.54,0,.05,.37,.25)],jacket)
    shape("Col du sous-vêtement",body,[(4.12,0,.032,.45,.37),(4.32,0,.05,.42,.37),(4.56,0,.05,.37,.32),(4.69,0,.056,.32,.28)],tealshade)
    shape("Ourlet de veste",body,[(2.78,0,.045,.64,.38),(2.83,0,.043,.73,.43),(2.94,0,.044,.75,.442),(3.01,0,.043,.707,.423)],ochre)
    shape("Bassin · pantalon",body,[(2.46,0,.073,.56,.34),(2.64,0,.071,.68,.38),(2.86,0,.055,.69,.40),(2.99,0,.043,.61,.35)],teal)

    for s in (-1,1):
        name="G" if s<0 else "D"
        shape("Pantalon "+name,body,[
            (.36,s*.51,.06,.25,.24),(.54,s*.52,.062,.28,.26),(.87,s*.53,.07,.27,.25),
            (1.24,s*.49,.016,.32,.29),(1.49,s*.47,-.022,.33,.32),(1.77,s*.43,.035,.35,.34),
            (2.17,s*.40,.045,.392,.365),(2.52,s*.345,.047,.395,.35),(2.73,s*.32,.061,.365,.33)
        ],teal)
        egg("Renfort de genou "+name,body,(s*.487,-.245,1.36),(.238,.104,.30),tealshade)
        line("Couture pantalon "+name,trim,[(s*.70,-.14,2.59),(s*.755,-.18,2.16),(s*.754,-.17,1.68),(s*.771,-.126,1.25),(s*.77,-.09,.66)],.017,tealshade)
        box("Semelle "+name,hands,(s*.54,-.115,.126),(.63,.93,.23),sock,.105)
        shape("Chaussure "+name,hands,[(.13,s*.54,-.12,.30,.45),(.22,s*.54,-.126,.30,.46),(.32,s*.535,-.11,.29,.43),(.42,s*.525,-.035,.27,.35),(.59,s*.52,.065,.251,.255)],tealshade)
        line("Protection d’orteil "+name,trim,[(s*.34,-.462,.25),(s*.43,-.529,.267),(s*.54,-.544,.270),(s*.664,-.522,.26),(s*.75,-.449,.245)],.038,sock)
        for n in range(3):
            dy=-.360+n*.070
            line("Lacet "+name,trim,[(s*.38,dy,.357+n*.024),(s*.52,dy-.036,.385+n*.022),(s*.67,dy,.356+n*.024)],.018,stitch)

        # The cut of the sleeve defines elbow and cuff changes before trim.
        arm=[((s*.48,.065,4.10),.283,.273),((s*.69,.05,4.18),.318,.309),
             ((s*.86,.032,4.16),.335,.328),
             ((s*1.047,.004,3.97),.315,.309),((s*1.145,-.019,3.62),.271,.258),
             ((s*1.208,-.078,3.35),.253,.245),((s*1.245,-.109,3.13),.230,.219),
             ((s*1.27,-.13,2.93),.209,.195),((s*1.285,-.14,2.81),.181,.168)]
        loft("Manche "+name,body,arm,jacket)
        loft("Poignet toile "+name,body,[
            ((s*1.258,-.125,3.02),.216,.200),((s*1.28,-.14,2.97),.215,.198),
            ((s*1.289,-.145,2.80),.192,.175),((s*1.297,-.151,2.765),.169,.156)],ochre)
        egg("Gant paume "+name,hands,(s*1.302,-.155,2.615),(.192,.146,.232),sock)
        for i in range(4):
            x=s*(1.177+i*.083)
            z=2.485-(.07 if i in (1,2) else .022)
            line("Doigt de gant "+name,hands,[(x,-.165,2.63,.93),(x+s*.015,-.171,z+.02,1),(x+s*.024,-.215,z-.06,.22)],.055,sock)
        line("Pouce de gant "+name,hands,[(s*1.191,-.19,2.69,.98),(s*1.12,-.223,2.57,1),(s*1.143,-.289,2.50,.26)],.075,sock)
        egg("Renfort dorsal "+name,hands,(s*1.32,-.275,2.63),(.122,.038,.117),tealshade)
        line("Surpiqûre manche "+name,trim,[(s*.79,-.255,4.33),(s*.98,-.275,4.08),(s*1.15,-.225,3.81),(s*1.23,-.239,3.43),(s*1.29,-.292,3.00)],.019,ochre)

    line("Zip de veste",trim,[(0,-.359,2.87),(0,-.398,3.24),(0,-.449,3.73),(0,-.426,4.24),(0,-.36,4.42)],.040,tealshade)
    for z in (3.0,3.25,3.50,3.75,4.0,4.22):
        y=-.423-.032*math.sin((z-3.0)*2.9)
        box("Maille métallique",trim,(0,y-.020,z),(.041,.018,.017),buck,.006)
    box("Curseur",trim,(0,-.450,4.17),(.093,.049,.151),buck,.016)
    box("Poche poitrine",trim,(-.42,-.366,3.85),(.43,.14,.37),ochre,.055)
    box("Rabat de poche",trim,(-.42,-.455,3.979),(.45,.057,.106),jacket,.025)
    box("Écusson",trim,(.407,-.41,4.027),(.32,.044,.14),tealshade,.023)
    for j in range(3):
        box("Barre d’écusson",trim,(.347+j*.061,-.436,4.026),(.024,.016,.058),stitch,.006)
    for s in (-1,1):
        line("Ouverture de poche",trim,[(s*.24,-.393,3.185),(s*.36,-.386,3.255),(s*.56,-.318,3.430)],.030,ochre)
    line("Col relevé gauche",trim,[(-.037,-.327,4.46,.55),(-.256,-.282,4.57,1),(-.393,-.096,4.63,1),(-.314,.125,4.63,.62)],.071,jacket)
    line("Col relevé droit",trim,[(.037,-.327,4.46,.55),(.256,-.282,4.57,1),(.393,-.096,4.63,1),(.314,.125,4.63,.62)],.071,jacket)

    scene=show(studio,(0,0,3.48),(10,-23,8.1),8.30,L.material("Fond · pétrole ardoise",(.105,.169,.188),.75),size=(980,1280))
    scene.unit_settings.system="METRIC"; scene.unit_settings.scale_length=.25
    cam=scene.camera; cam.name="CAM_Corps"
    close=L.camera("CAM_Visage",studio,location=(5.4,-14,7.0),make_active=False)
    close.rotation_euler=(Vector((0,-.02,5.86))-close.location).to_track_quat("-Z","Y").to_euler()
    close.data.type="ORTHO"; close.data.ortho_scale=2.50
    for name, eye in (("CAM_Face",(0,-18,5.87)),("CAM_Profil",(15,0,5.87))):
        c=L.camera(name,studio,location=eye,make_active=False)
        c.rotation_euler=(Vector((0,0,5.86))-c.location).to_track_quat("-Z","Y").to_euler()
        c.data.type="ORTHO"; c.data.ortho_scale=2.45
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type=="VIEW_3D" and area.spaces.active.region_3d:
                area.spaces.active.region_3d.view_perspective="CAMERA"
    bpy.ops.object.select_all(action="DESELECT")
    note=bpy.data.texts.new("NORA · fiche du prototype")
    note.write(
        "Personnage stylisé original. Les caméras Corps, Visage, Face et Profil servent à la revue. "
        + ("GEO_Tete_Cou_Continu est une surface fermée et connectée, du crâne à la base du cou. " if continuous else "")
        + "Les surfaces des yeux, les bords de paupières, les lèvres, les oreilles et la coiffure restent séparés. "
        "Corps habillé en pose neutre. Prototype avant retopologie et rig."
    )
    return scene,close


def main():
    continuous = "continu" in L.args_after_dashdash()
    scene,close=build(continuous)
    suffix="_continu" if continuous else ""
    scene.render.filepath=f"//nora_corps{suffix}.png"
    L.save(str(HERE/f"nora_personnage{suffix}.blend"))
    if not continuous:
        bpy.ops.render.render(write_still=True)
    scene.camera=close
    scene.render.resolution_x=1024
    scene.render.resolution_y=1024
    scene.render.filepath=f"//nora_visage{suffix}.png"
    bpy.ops.render.render(write_still=True)
    if continuous:
        scene.camera=bpy.data.objects["CAM_Profil"]
        direction=Vector((0,0,5.63))-scene.camera.location
        scene.camera.rotation_euler=direction.to_track_quat("-Z","Y").to_euler()
        scene.camera.data.ortho_scale=2.8
        scene.render.filepath="//nora_profil_continu.png"
        bpy.ops.render.render(write_still=True)


if __name__=="__main__":
    L.run(main)
