# %% [markdown]
# # 🌍 Magellan's World Tour: The First Circumnavigation (1519–1522)
# #
# An animated globe visualization tracing Ferdinand Magellan's historic expedition
# from Sanlúcar de Barrameda, Spain, across the Atlantic, through the Strait of Magellan,
# across the Pacific, to the Philippines (where Magellan died), and the return journey
# under Juan Sebastián Elcano back to Spain.
# 
# 

# %%
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import FancyBboxPatch
from IPython.display import HTML
import json
import urllib.request

# %% [markdown]
# ## Define the Historical Route & Waypoints
# #
# We reconstruct the key waypoints of Magellan's expedition based on historical records.
# Each waypoint includes coordinates, dates, and a brief description of what happened there.
# 
# 

# %%
# Key waypoints of Magellan's expedition
# Format: (name, latitude, longitude, date, description)
waypoints = [
    ("Sanlúcar de Barrameda", 36.78, -6.35, "20 Sep 1519",
     "Departure: 5 ships & 270 men\nset sail as the 'Armada de Molucca'"),
    ("Canary Islands", 28.1, -15.4, "26 Sep 1519",
     "Brief stop for provisions\nat the Canary Islands"),
    ("Cape Verde", 14.9, -23.5, "Oct 1519",
     "Sailing south along the\nAfrican coast toward the equator"),
    ("Rio de Janeiro", -22.9, -43.2, "13 Dec 1519",
     "Arrival at the coast of Brazil;\nresupply and rest for the crew"),
    ("Río de la Plata", -34.6, -58.4, "Jan 1520",
     "Explored the estuary hoping\nit was a passage to the Pacific"),
    ("Puerto San Julián", -49.3, -67.7, "Mar–Aug 1520",
     "Wintered here 5 months;\ncrushed a mutiny of 3 captains"),
    ("Strait of Magellan", -52.5, -70.0, "21 Oct 1520",
     "Discovered the strait! 38-day\npassage through treacherous waters"),
    ("Pacific Ocean Entry", -52.0, -75.0, "28 Nov 1520",
     "Entered the 'Mar Pacifico'—\nMagellan wept with joy"),
    ("Mid-Pacific", -20.0, -130.0, "Jan 1521",
     "Grueling 99-day Pacific crossing;\nscurvy, starvation, and thirst"),
    ("Guam", 13.44, 144.79, "6 Mar 1521",
     "First Pacific landfall!\nCalled it 'Islas de los Ladrones'"),
    ("Cebu, Philippines", 10.3, 123.9, "7 Apr 1521",
     "Allied with Rajah Humabon;\nmass conversions to Christianity"),
    ("Mactan, Philippines", 10.31, 124.0, "27 Apr 1521",
     "⚔️ MAGELLAN KILLED in battle\nagainst Chief Lapu-Lapu"),
    ("Brunei", 4.9, 114.9, "Jul 1521",
     "Under new leadership, the fleet\nreached the Sultan of Brunei"),
    ("Tidore, Moluccas", 1.7, 127.4, "Nov 1521",
     "🌿 THE SPICE ISLANDS at last!\nLoaded cloves, nutmeg, cinnamon"),
    ("Timor", -10.2, 123.6, "Feb 1522",
     "Elcano's Victoria departs west;\nTrinidad tries east (fails)"),
    ("Indian Ocean", -20.0, 80.0, "Mar–Apr 1522",
     "Crossing the Indian Ocean;\navoiding Portuguese patrols"),
    ("Cape of Good Hope", -34.4, 18.5, "May 1522",
     "Rounding Africa's southern tip;\nship leaking, crew starving"),
    ("Cape Verde (return)", 14.9, -23.5, "Jul 1522",
     "Desperate stop for food;\n13 men arrested by Portuguese"),
    ("Sanlúcar de Barrameda", 36.78, -6.35, "6 Sep 1522",
     "🏆 FIRST CIRCUMNAVIGATION!\nOnly 18 of 270 men survived"),
]

# Extract coordinates for the route line
route_lats = [w[1] for w in waypoints]
route_lons = [w[2] for w in waypoints]
route_names = [w[0] for w in waypoints]
route_dates = [w[3] for w in waypoints]
route_descs = [w[4] for w in waypoints]

# Create a smooth interpolated route
def interpolate_route(lats, lons, points_per_segment=30):
    """Interpolate between waypoints for smooth animation."""
    smooth_lats, smooth_lons = [], []
    for i in range(len(lats) - 1):
        lat_seg = np.linspace(lats[i], lats[i+1], points_per_segment, endpoint=False)
        
        # Handle longitude wrapping (crossing the date line)
        lon_start, lon_end = lons[i], lons[i+1]
        diff = lon_end - lon_start
        if abs(diff) > 180:
            if diff > 0:
                lon_end -= 360
            else:
                lon_end += 360
        lon_seg = np.linspace(lon_start, lon_end, points_per_segment, endpoint=False)
        # Normalize back to -180..180
        lon_seg = ((lon_seg + 180) % 360) - 180
        
        smooth_lats.extend(lat_seg)
        smooth_lons.extend(lon_seg)
    smooth_lats.append(lats[-1])
    smooth_lons.append(lons[-1])
    return np.array(smooth_lats), np.array(smooth_lons)

smooth_lats, smooth_lons = interpolate_route(route_lats, route_lons, points_per_segment=25)
print(f"Route: {len(waypoints)} waypoints → {len(smooth_lats)} animation frames")



# %% [markdown]
# ## Globe Rendering Engine
# 
# We load real-world coastline geometry from Natural Earth (110m resolution) for accurate
# continent shapes, then render them on an orthographic projection globe.

# %%
# Load real coastline data from Natural Earth (110m cultural vectors)
url = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_land.geojson"

try:
    print("Downloading Natural Earth coastline data...")
    with urllib.request.urlopen(url, timeout=15) as resp:
        geo = json.loads(resp.read().decode())
    
    continents = []
    for feature in geo['features']:
        geom = feature['geometry']
        if geom['type'] == 'Polygon':
            for ring in geom['coordinates']:
                coords = np.array(ring)
                continents.append((coords[:, 1].tolist(), coords[:, 0].tolist()))  # (lats, lons)
        elif geom['type'] == 'MultiPolygon':
            for polygon in geom['coordinates']:
                for ring in polygon:
                    coords = np.array(ring)
                    continents.append((coords[:, 1].tolist(), coords[:, 0].tolist()))
    
    print(f"Loaded {len(continents)} land polygons from Natural Earth")
    USE_REAL_DATA = True

except Exception as e:
    print(f"Could not download Natural Earth data: {e}")
    print("Falling back to built-in outlines...")
    USE_REAL_DATA = False

    # Fallback simplified continents (only used if download fails)
    continents = []
    
    # Africa
    continents.append((
        [37,36,35,33,32,31,30,28,25,22,19,16,12,8,5,2,0,-2,-5,-8,-12,-16,-20,-24,-28,-31,-34,-34,-33,-30,-26,-22,-18,-14,-10,-6,-2,2,5,8,10,12,14,15,37],
        [-5,-2,0,3,10,15,20,25,30,33,37,40,42,44,45,44,42,41,40,39,40,36,35,34,32,30,26,18,15,12,10,9,8,7,5,2,-1,-3,-5,-8,-10,-13,-15,-17,-5]
    ))
    # South America
    continents.append((
        [12,10,8,5,2,0,-3,-8,-15,-22,-28,-34,-40,-48,-54,-55,-52,-48,-42,-35,-28,-20,-12,-5,0,5,8,10,12],
        [-72,-68,-63,-58,-52,-50,-48,-42,-40,-38,-40,-48,-55,-62,-68,-70,-75,-78,-75,-72,-70,-72,-75,-78,-80,-78,-75,-72,-72]
    ))
    # North America
    continents.append((
        [10,15,20,25,30,32,34,40,45,50,55,60,65,70,72,70,65,60,55,50,45,42,40,35,30,25,20,15,10],
        [-82,-88,-95,-100,-105,-110,-118,-124,-128,-130,-140,-155,-168,-165,-140,-120,-110,-100,-90,-85,-80,-75,-70,-75,-80,-82,-85,-88,-82]
    ))
    # Eurasia
    continents.append((
        [37,38,40,43,46,48,50,52,55,58,60,62,65,68,70,72,71,70,68,65,62,60,58,55,50,45,42,40,38,37,36,35,37,40,42,45,50,55,60,65,68,70,68,65,60,55,50,45,40,38,37],
        [-10,-5,0,5,8,3,0,5,10,15,20,25,28,30,35,40,50,60,70,80,85,90,95,100,105,110,115,120,125,130,135,140,142,140,135,130,128,130,135,140,150,160,170,175,170,160,150,140,130,125,-10]
    ))
    # Australia
    continents.append((
        [-15,-12,-13,-15,-20,-25,-30,-35,-38,-37,-33,-28,-22,-18,-15],
        [125,130,135,140,145,150,153,152,148,142,138,132,128,122,125]
    ))
    
    print(f"Using {len(continents)} fallback continent outlines")
    USE_REAL_DATA = False

# Convert to dict format for compatibility
continents_dict = {}
for i, (lats, lons) in enumerate(continents):
    continents_dict[f'land_{i}'] = (lats, lons)

print(f"Total land polygons ready: {len(continents_dict)}")

# %%
def project_orthographic(lat, lon, center_lat, center_lon):
    """Project lat/lon to orthographic (globe) x, y coordinates."""
    lat_r = np.radians(np.asarray(lat, dtype=float))
    lon_r = np.radians(np.asarray(lon, dtype=float))
    clat_r = np.radians(center_lat)
    clon_r = np.radians(center_lon)

    cos_c = (np.sin(clat_r) * np.sin(lat_r) +
             np.cos(clat_r) * np.cos(lat_r) * np.cos(lon_r - clon_r))

    x = np.cos(lat_r) * np.sin(lon_r - clon_r)
    y = (np.cos(clat_r) * np.sin(lat_r) -
         np.sin(clat_r) * np.cos(lat_r) * np.cos(lon_r - clon_r))

    visible = cos_c > 0
    return x, y, visible


def draw_globe(ax, center_lat, center_lon, route_idx, cont_dict,
               smooth_lats, smooth_lons, waypoints, route_lats, route_lons):
    """Draw globe with realistic Natural Earth landmasses on #1e1e1e background."""
    ax.clear()
    ax.set_facecolor('#1e1e1e')
    ax.set_xlim(-1.45, 1.45)
    ax.set_ylim(-1.45, 1.45)
    ax.set_aspect('equal')
    ax.axis('off')

    theta = np.linspace(0, 2 * np.pi, 300)

    # Ocean
    ax.fill(np.cos(theta), np.sin(theta), color='#0a1628', zorder=1)
    ax.plot(np.cos(theta), np.sin(theta), color='#2a4a7f', linewidth=1.0, zorder=2)

    # Graticule
    for lat_line in range(-60, 90, 30):
        lons_g = np.linspace(-180, 180, 500)
        lats_g = np.full_like(lons_g, lat_line)
        x, y, vis = project_orthographic(lats_g, lons_g, center_lat, center_lon)
        x[~vis] = np.nan
        y[~vis] = np.nan
        ax.plot(x, y, color='#152a4a', linewidth=0.3, zorder=2)

    for lon_line in range(-180, 180, 30):
        lats_g = np.linspace(-90, 90, 250)
        lons_g = np.full_like(lats_g, lon_line)
        x, y, vis = project_orthographic(lats_g, lons_g, center_lat, center_lon)
        x[~vis] = np.nan
        y[~vis] = np.nan
        ax.plot(x, y, color='#152a4a', linewidth=0.3, zorder=2)

    # Equator
    lons_eq = np.linspace(-180, 180, 500)
    lats_eq = np.zeros_like(lons_eq)
    x, y, vis = project_orthographic(lats_eq, lons_eq, center_lat, center_lon)
    x[~vis] = np.nan
    y[~vis] = np.nan
    ax.plot(x, y, color='#1e3a60', linewidth=0.5, linestyle='--', zorder=2)

    # Draw land polygons
    for name, (clats, clons) in cont_dict.items():
        clats_a = np.array(clats, dtype=float)
        clons_a = np.array(clons, dtype=float)
        x, y, vis = project_orthographic(clats_a, clons_a, center_lat, center_lon)

        # Split into visible contiguous segments and clip to globe
        # For filled polygons we need contiguous visible points
        vis_x = x[vis]
        vis_y = y[vis]

        if len(vis_x) < 3:
            continue

        # Clip to unit circle
        dist = np.sqrt(vis_x**2 + vis_y**2)
        mask = dist <= 1.0
        if np.sum(mask) < 3:
            continue

        ax.fill(vis_x, vis_y, color='#1e3e1e', alpha=0.9, zorder=3)
        ax.plot(vis_x, vis_y, color='#3a7a3a', linewidth=0.5, zorder=4)

    # Completed route
    if route_idx > 0:
        rx, ry = [], []
        for i in range(min(route_idx, len(smooth_lats))):
            x, y, vis = project_orthographic(
                np.array([smooth_lats[i]]), np.array([smooth_lons[i]]),
                center_lat, center_lon)
            if vis[0]:
                rx.append(x[0]); ry.append(y[0])
            else:
                rx.append(np.nan); ry.append(np.nan)

        if rx:
            ax.plot(rx, ry, color='#ff6b35', linewidth=3.0, alpha=0.2, zorder=5)
            ax.plot(rx, ry, color='#ff8844', linewidth=1.8, alpha=0.4, zorder=5)
            ax.plot(rx, ry, color='#ffcc00', linewidth=0.9, alpha=0.85, zorder=6)

    # Waypoint markers
    points_per_seg = max(len(smooth_lats) // (len(waypoints) - 1), 1)
    for i, wp in enumerate(waypoints):
        wp_frame = i * points_per_seg
        if wp_frame <= route_idx:
            x, y, vis = project_orthographic(
                np.array([wp[1]]), np.array([wp[2]]), center_lat, center_lon)
            if vis[0]:
                if "KILLED" in wp[4]:
                    ax.plot(x[0], y[0], 'x', color='#ff0000', markersize=12,
                            markeredgewidth=3, zorder=8)
                    ax.plot(x[0], y[0], 'o', color='#ff0000', markersize=16,
                            markerfacecolor='none', markeredgewidth=1.5, alpha=0.6, zorder=7)
                elif "CIRCUMNAVIGATION" in wp[4]:
                    ax.plot(x[0], y[0], '*', color='#ffd700', markersize=18, zorder=8)
                else:
                    ax.plot(x[0], y[0], 'o', color='#ffaa00', markersize=5,
                            markeredgecolor='#ff6b35', markeredgewidth=1.2, zorder=8)

    # Current position
    if route_idx < len(smooth_lats):
        curr_lat = smooth_lats[route_idx]
        curr_lon = smooth_lons[route_idx]
        x, y, vis = project_orthographic(
            np.array([curr_lat]), np.array([curr_lon]),
            center_lat, center_lon)
        if vis[0]:
            pulse = 8 + 4 * np.sin(route_idx * 0.3)
            ax.plot(x[0], y[0], 'o', color='#ff4444', markersize=pulse,
                    markerfacecolor='none', markeredgewidth=2, alpha=0.6, zorder=9)
            ax.plot(x[0], y[0], 'o', color='#ffffff', markersize=5, zorder=10)

    # Determine current waypoint
    current_wp_idx = min(route_idx // points_per_seg, len(waypoints) - 1)
    wp = waypoints[current_wp_idx]

    return wp, current_wp_idx

# %% [markdown]
# ## Create the Animation
# #
# The globe rotates to follow Magellan's ship as it progresses along the route.
# Historical information is displayed for each waypoint reached.
# 
# 

# %%
# Animation setup
fig = plt.figure(figsize=(14, 9), facecolor='#1e1e1e')

ax_globe = fig.add_axes([0.02, 0.05, 0.6, 0.88])
ax_info = fig.add_axes([0.64, 0.05, 0.34, 0.88])
ax_info.set_facecolor('#1e1e1e')
ax_info.axis('off')

fig.text(0.5, 0.97, "MAGELLAN'S EXPEDITION: THE FIRST CIRCUMNAVIGATION",
         fontsize=16, fontweight='bold', color='#ffaa00',
         ha='center', va='top', fontfamily='monospace')
fig.text(0.5, 0.935, "1519 \u2013 1522  \u00b7  Sanl\u00facar de Barrameda \u2192 Around the World",
         fontsize=10, color='#888888', ha='center', va='top', fontfamily='monospace')

n_frames = len(smooth_lats)
points_per_seg = n_frames // (len(waypoints) - 1)

# Target 30 seconds at 30fps
target_duration = 30.0
target_fps = 30
total_anim_frames = int(target_duration * target_fps)
speed_main = max(n_frames / total_anim_frames, 1.0)

ship_data = [
    (0, 5, 270, "Departure"),
    (5, 5, 265, "Atlantic Crossing"),
    (6, 4, 250, "Mutiny crushed; Santiago lost"),
    (7, 3, 240, "San Antonio deserts"),
    (11, 3, 200, "Magellan killed"),
    (12, 2, 150, "Concepci\u00f3n burned"),
    (14, 2, 130, "Trinidad & Victoria split"),
    (18, 1, 18, "Only Victoria returns"),
]

def get_fleet_status(wp_idx):
    ships, crew, note = 5, 270, "Full fleet"
    for threshold, s, c, n in ship_data:
        if wp_idx >= threshold:
            ships, crew, note = s, c, n
    return ships, crew, note


def animate(frame):
    route_idx = min(int(frame * speed_main), n_frames - 1)
    curr_lat = smooth_lats[route_idx]
    curr_lon = smooth_lons[route_idx]
    center_lat = curr_lat * 0.3
    center_lon = curr_lon

    wp, wp_idx = draw_globe(ax_globe, center_lat, center_lon, route_idx,
                            continents_dict, smooth_lats, smooth_lons,
                            waypoints, route_lats, route_lons)

    # Info panel
    ax_info.clear()
    ax_info.set_facecolor('#1e1e1e')
    ax_info.set_xlim(0, 1)
    ax_info.set_ylim(0, 1)
    ax_info.axis('off')

    progress = route_idx / max(n_frames - 1, 1)
    ax_info.fill_between([0.05, 0.95], [0.96, 0.96], [0.97, 0.97],
                         color='#333333', zorder=1)
    ax_info.fill_between([0.05, 0.05 + 0.9 * progress], [0.96, 0.96], [0.97, 0.97],
                         color='#ffaa00', alpha=0.8, zorder=2)
    ax_info.text(0.5, 0.985, f"VOYAGE PROGRESS: {progress*100:.0f}%",
                 fontsize=8, color='#aaaaaa', ha='center', fontfamily='monospace')

    ax_info.text(0.5, 0.91, f"\U0001f4cd {wp[0].upper()}", fontsize=13, fontweight='bold',
                 color='#ffaa00', ha='center', fontfamily='monospace')
    ax_info.text(0.5, 0.87, f"\U0001f4c5 {wp[3]}", fontsize=10, color='#cccccc',
                 ha='center', fontfamily='monospace')

    lat_str = f"{abs(wp[1]):.1f}\u00b0{'N' if wp[1] >= 0 else 'S'}"
    lon_str = f"{abs(wp[2]):.1f}\u00b0{'E' if wp[2] >= 0 else 'W'}"
    ax_info.text(0.5, 0.83, f"{lat_str}, {lon_str}", fontsize=9,
                 color='#888888', ha='center', fontfamily='monospace')

    ax_info.plot([0.1, 0.9], [0.80, 0.80], color='#444444', linewidth=1)

    desc_lines = wp[4].split('\n')
    for i, line in enumerate(desc_lines):
        ax_info.text(0.5, 0.76 - i * 0.04, line, fontsize=10, color='#dddddd',
                     ha='center', fontfamily='monospace')

    ax_info.plot([0.1, 0.9], [0.65, 0.65], color='#444444', linewidth=1)

    ships, crew, note = get_fleet_status(wp_idx)
    ax_info.text(0.5, 0.61, "FLEET STATUS", fontsize=10, fontweight='bold',
                 color='#ff6b35', ha='center', fontfamily='monospace')

    ship_str = "\u26f5" * ships + "  \U0001f480" * (5 - ships)
    ax_info.text(0.5, 0.56, ship_str, fontsize=14, ha='center')

    ax_info.text(0.5, 0.51, f"Ships: {ships}/5  \u00b7  Crew: ~{crew}/270",
                 fontsize=9, color='#cccccc', ha='center', fontfamily='monospace')
    ax_info.text(0.5, 0.47, note, fontsize=8, color='#ff6b35',
                 ha='center', fontfamily='monospace', style='italic')

    ax_info.plot([0.1, 0.9], [0.43, 0.43], color='#444444', linewidth=1)

    if wp_idx < 11:
        commander = "Ferdinand Magellan"
        cmd_color = '#ffaa00'
        nationality = "Portuguese navigator\nserving the Spanish Crown"
    else:
        commander = "Juan Sebasti\u00e1n Elcano"
        cmd_color = '#66bbff'
        nationality = "Spanish navigator\ncompleting the voyage"

    ax_info.text(0.5, 0.39, "COMMANDER", fontsize=10, fontweight='bold',
                 color=cmd_color, ha='center', fontfamily='monospace')
    ax_info.text(0.5, 0.35, commander, fontsize=11, color='#ffffff',
                 ha='center', fontfamily='monospace', fontweight='bold')
    nat_lines = nationality.split('\n')
    for i, line in enumerate(nat_lines):
        ax_info.text(0.5, 0.31 - i * 0.035, line, fontsize=8, color='#999999',
                     ha='center', fontfamily='monospace')

    ax_info.plot([0.1, 0.9], [0.23, 0.23], color='#444444', linewidth=1)

    ax_info.text(0.5, 0.19, "WAYPOINTS REACHED", fontsize=9, fontweight='bold',
                 color='#66bbff', ha='center', fontfamily='monospace')

    start_wp = max(0, wp_idx - 4)
    for i in range(start_wp, min(wp_idx + 1, len(waypoints))):
        y_pos = 0.15 - (i - start_wp) * 0.03
        if y_pos < 0.02:
            break
        marker = "\u25b6" if i == wp_idx else "\u2022"
        color = '#ffaa00' if i == wp_idx else '#666666'
        ax_info.text(0.08, y_pos, f"{marker} {waypoints[i][0]}",
                     fontsize=7, color=color, fontfamily='monospace')
        ax_info.text(0.92, y_pos, waypoints[i][3],
                     fontsize=7, color='#555555', ha='right', fontfamily='monospace')

    return []

interval_ms = int(1000 / target_fps)
anim = animation.FuncAnimation(fig, animate, frames=total_anim_frames,
                               interval=interval_ms, blit=False, repeat=True)

plt.close(fig)
print(f"Main animation: {total_anim_frames} frames at {target_fps}fps")
print(f"Duration: ~{total_anim_frames / target_fps:.1f} seconds")
print(f"Route speed: {speed_main:.2f} route points per frame")
print("Rendering HTML5 video...")

# %% [markdown]
# ## 🎬 Watch the Animation
# #
# The globe rotates to follow Magellan's fleet as it sails around the world.
# The info panel on the right shows current location, date, fleet status, and historical context.
# 
# 

# %%
# Display the animation
HTML(anim.to_html5_video())



# %% [markdown]
# ## 📱 YouTube Shorts Version (9:16 Vertical)
# 
# A vertical-format animation optimized for YouTube Shorts (~30 seconds at 30fps).

# %%
# YouTube Shorts animation - 9:16 vertical format, #1e1e1e background
# Target: ~30 seconds at 30fps = ~900 frames

fig_yt = plt.figure(figsize=(6, 10.67), facecolor='#1e1e1e', dpi=180)

ax_globe_yt = fig_yt.add_axes([0.02, 0.30, 0.96, 0.54])
ax_top = fig_yt.add_axes([0.0, 0.85, 1.0, 0.15])
ax_bot = fig_yt.add_axes([0.0, 0.0, 1.0, 0.30])

for a in [ax_top, ax_bot]:
    a.set_facecolor('#1e1e1e')
    a.axis('off')

n_frames_yt = len(smooth_lats)
points_per_seg_yt = n_frames_yt // (len(waypoints) - 1)

target_duration_yt = 30.0
target_fps_yt = 30
total_yt_frames = int(target_duration_yt * target_fps_yt)
speed_yt = max(n_frames_yt / total_yt_frames, 1.0)

def animate_yt(frame):
    route_idx = min(int(frame * speed_yt), n_frames_yt - 1)
    curr_lat = smooth_lats[route_idx]
    curr_lon = smooth_lons[route_idx]
    center_lat = curr_lat * 0.3
    center_lon = curr_lon

    wp, wp_idx = draw_globe(ax_globe_yt, center_lat, center_lon, route_idx,
                            continents_dict, smooth_lats, smooth_lons,
                            waypoints, route_lats, route_lons)

    ax_top.clear()
    ax_top.set_facecolor('#1e1e1e')
    ax_top.set_xlim(0, 1)
    ax_top.set_ylim(0, 1)
    ax_top.axis('off')

    ax_top.text(0.5, 0.82, "MAGELLAN'S EXPEDITION", fontsize=15, fontweight='bold',
                color='#ffaa00', ha='center', fontfamily='monospace')
    ax_top.text(0.5, 0.58, "The First Circumnavigation \u00b7 1519\u20131522",
                fontsize=8, color='#888888', ha='center', fontfamily='monospace')

    progress = route_idx / max(n_frames_yt - 1, 1)
    bar_y = 0.30
    ax_top.fill_between([0.08, 0.92], [bar_y, bar_y], [bar_y + 0.10, bar_y + 0.10],
                        color='#2a2a2a', zorder=1)
    ax_top.fill_between([0.08, 0.08 + 0.84 * progress], [bar_y, bar_y],
                        [bar_y + 0.10, bar_y + 0.10], color='#ffaa00', alpha=0.85, zorder=2)
    ax_top.text(0.5, bar_y + 0.05, f"{progress*100:.0f}%", fontsize=7,
                color='#1e1e1e' if progress > 0.4 else '#aaaaaa',
                ha='center', va='center', fontfamily='monospace', fontweight='bold', zorder=3)

    ax_bot.clear()
    ax_bot.set_facecolor('#1e1e1e')
    ax_bot.set_xlim(0, 1)
    ax_bot.set_ylim(0, 1)
    ax_bot.axis('off')

    ax_bot.text(0.5, 0.92, wp[0].upper(), fontsize=13, fontweight='bold',
                color='#ffaa00', ha='center', fontfamily='monospace')
    ax_bot.text(0.5, 0.82, wp[3], fontsize=10, color='#cccccc',
                ha='center', fontfamily='monospace')

    ax_bot.plot([0.15, 0.85], [0.76, 0.76], color='#444444', linewidth=0.8)

    desc_lines = wp[4].split('\n')
    for i, line in enumerate(desc_lines):
        ax_bot.text(0.5, 0.68 - i * 0.08, line, fontsize=9, color='#dddddd',
                    ha='center', fontfamily='monospace')

    ax_bot.plot([0.15, 0.85], [0.48, 0.48], color='#444444', linewidth=0.8)

    ships, crew, note = get_fleet_status(wp_idx)
    ship_str = "\u26f5" * ships + "  \u2620" * (5 - ships)
    ax_bot.text(0.5, 0.38, ship_str, fontsize=14, ha='center', color='#cccccc')
    ax_bot.text(0.5, 0.26, f"Ships: {ships}/5  \u00b7  Crew: ~{crew}/270",
                fontsize=8, color='#aaaaaa', ha='center', fontfamily='monospace')

    if wp_idx < 11:
        cmd = "Cmd: Ferdinand Magellan"
        cmd_c = '#ffaa00'
    else:
        cmd = "Cmd: Juan Sebasti\u00e1n Elcano"
        cmd_c = '#66bbff'
    ax_bot.text(0.5, 0.14, cmd, fontsize=8, color=cmd_c,
                ha='center', fontfamily='monospace', fontweight='bold')
    ax_bot.text(0.5, 0.04, note, fontsize=7, color='#ff6b35',
                ha='center', fontfamily='monospace', style='italic')

    return []

interval_ms_yt = int(1000 / target_fps_yt)
anim_yt = animation.FuncAnimation(fig_yt, animate_yt, frames=total_yt_frames,
                                   interval=interval_ms_yt, blit=False, repeat=True)

plt.close(fig_yt)
print(f"YouTube Shorts animation: {total_yt_frames} frames at {target_fps_yt}fps")
print(f"Duration: ~{total_yt_frames / target_fps_yt:.1f} seconds")
print(f"Route speed: {speed_yt:.2f} route points per frame")
print("Rendering HTML5 video...")

# %%
HTML(anim_yt.to_html5_video())

# %% [markdown]
# ## 🐦 Twitter/X Version (1:1 Square)
# 
# A square-format animation optimized for Twitter/X posts (~30 seconds at 30fps).

# %%
# Twitter/X animation - 1:1 square format, #1e1e1e background
# Target: ~30 seconds at 30fps = ~900 frames

fig_tw = plt.figure(figsize=(8, 8), facecolor='#1e1e1e', dpi=150)

ax_globe_tw = fig_tw.add_axes([0.02, 0.18, 0.96, 0.68])
ax_top_tw = fig_tw.add_axes([0.0, 0.87, 1.0, 0.13])
ax_bot_tw = fig_tw.add_axes([0.0, 0.0, 1.0, 0.18])

for a in [ax_top_tw, ax_bot_tw]:
    a.set_facecolor('#1e1e1e')
    a.axis('off')

n_frames_tw = len(smooth_lats)
target_duration_tw = 30.0
target_fps_tw = 30
total_tw_frames = int(target_duration_tw * target_fps_tw)
speed_tw = max(n_frames_tw / total_tw_frames, 1.0)

def animate_tw(frame):
    route_idx = min(int(frame * speed_tw), n_frames_tw - 1)
    curr_lat = smooth_lats[route_idx]
    curr_lon = smooth_lons[route_idx]
    center_lat = curr_lat * 0.3
    center_lon = curr_lon

    wp, wp_idx = draw_globe(ax_globe_tw, center_lat, center_lon, route_idx,
                            continents_dict, smooth_lats, smooth_lons,
                            waypoints, route_lats, route_lons)

    # Top panel
    ax_top_tw.clear()
    ax_top_tw.set_facecolor('#1e1e1e')
    ax_top_tw.set_xlim(0, 1)
    ax_top_tw.set_ylim(0, 1)
    ax_top_tw.axis('off')

    ax_top_tw.text(0.5, 0.75, "MAGELLAN'S EXPEDITION \u00b7 1519\u20131522",
                   fontsize=13, fontweight='bold', color='#ffaa00',
                   ha='center', fontfamily='monospace')

    progress = route_idx / max(n_frames_tw - 1, 1)
    ax_top_tw.fill_between([0.10, 0.90], [0.20, 0.20], [0.35, 0.35],
                           color='#2a2a2a', zorder=1)
    ax_top_tw.fill_between([0.10, 0.10 + 0.80 * progress], [0.20, 0.20],
                           [0.35, 0.35], color='#ffaa00', alpha=0.85, zorder=2)
    ax_top_tw.text(0.5, 0.275, f"{progress*100:.0f}%", fontsize=7,
                   color='#1e1e1e' if progress > 0.4 else '#aaaaaa',
                   ha='center', va='center', fontfamily='monospace', fontweight='bold', zorder=3)

    # Bottom panel
    ax_bot_tw.clear()
    ax_bot_tw.set_facecolor('#1e1e1e')
    ax_bot_tw.set_xlim(0, 1)
    ax_bot_tw.set_ylim(0, 1)
    ax_bot_tw.axis('off')

    ax_bot_tw.text(0.02, 0.75, f"\U0001f4cd {wp[0]}", fontsize=11, fontweight='bold',
                   color='#ffaa00', ha='left', fontfamily='monospace')
    ax_bot_tw.text(0.98, 0.75, wp[3], fontsize=10, color='#cccccc',
                   ha='right', fontfamily='monospace')

    desc_line = wp[4].replace('\n', ' \u00b7 ')
    ax_bot_tw.text(0.5, 0.42, desc_line, fontsize=8, color='#dddddd',
                   ha='center', fontfamily='monospace')

    ships, crew, note = get_fleet_status(wp_idx)
    ship_str = "\u26f5" * ships + " \u2620" * (5 - ships)
    if wp_idx < 11:
        cmd = "Magellan"
        cmd_c = '#ffaa00'
    else:
        cmd = "Elcano"
        cmd_c = '#66bbff'
    ax_bot_tw.text(0.02, 0.08, f"{ship_str}  {ships}/5 ships  \u00b7  ~{crew} crew",
                   fontsize=8, color='#aaaaaa', ha='left', fontfamily='monospace')
    ax_bot_tw.text(0.98, 0.08, f"Cmd: {cmd}", fontsize=8, color=cmd_c,
                   ha='right', fontfamily='monospace', fontweight='bold')

    return []

interval_ms_tw = int(1000 / target_fps_tw)
anim_tw = animation.FuncAnimation(fig_tw, animate_tw, frames=total_tw_frames,
                                   interval=interval_ms_tw, blit=False, repeat=True)

plt.close(fig_tw)
print(f"Twitter/X animation: {total_tw_frames} frames at {target_fps_tw}fps")
print(f"Duration: ~{total_tw_frames / target_fps_tw:.1f} seconds")
print(f"Format: 1:1 square (1200x1200 at 150dpi)")
print(f"Route speed: {speed_tw:.2f} route points per frame")
print("Rendering HTML5 video...")

# %%
HTML(anim_tw.to_html5_video())

# %% [markdown]
# ## 📸 Instagram Reels Version (9:16 Vertical)
# 
# A vertical-format animation optimized for Instagram Reels (~30 seconds at 30fps).
# Similar to YouTube Shorts but with Instagram-style layout tweaks.

# %%
# Instagram Reels animation - 9:16 vertical format, #1e1e1e background
# Target: ~30 seconds at 30fps = ~900 frames

fig_ig = plt.figure(figsize=(6, 10.67), facecolor='#1e1e1e', dpi=180)

ax_globe_ig = fig_ig.add_axes([0.0, 0.28, 1.0, 0.56])
ax_top_ig = fig_ig.add_axes([0.0, 0.85, 1.0, 0.15])
ax_bot_ig = fig_ig.add_axes([0.0, 0.0, 1.0, 0.28])

for a in [ax_top_ig, ax_bot_ig]:
    a.set_facecolor('#1e1e1e')
    a.axis('off')

n_frames_ig = len(smooth_lats)
target_duration_ig = 30.0
target_fps_ig = 30
total_ig_frames = int(target_duration_ig * target_fps_ig)
speed_ig = max(n_frames_ig / total_ig_frames, 1.0)

def animate_ig(frame):
    route_idx = min(int(frame * speed_ig), n_frames_ig - 1)
    curr_lat = smooth_lats[route_idx]
    curr_lon = smooth_lons[route_idx]
    center_lat = curr_lat * 0.3
    center_lon = curr_lon

    wp, wp_idx = draw_globe(ax_globe_ig, center_lat, center_lon, route_idx,
                            continents_dict, smooth_lats, smooth_lons,
                            waypoints, route_lats, route_lons)

    # Top panel - Instagram style with rounded feel
    ax_top_ig.clear()
    ax_top_ig.set_facecolor('#1e1e1e')
    ax_top_ig.set_xlim(0, 1)
    ax_top_ig.set_ylim(0, 1)
    ax_top_ig.axis('off')

    ax_top_ig.text(0.5, 0.80, "\u2693 MAGELLAN'S EXPEDITION", fontsize=14, fontweight='bold',
                   color='#ffaa00', ha='center', fontfamily='monospace')
    ax_top_ig.text(0.5, 0.55, "First Circumnavigation of Earth",
                   fontsize=8, color='#aaaaaa', ha='center', fontfamily='monospace')
    ax_top_ig.text(0.5, 0.38, "1519 \u2014 1522",
                   fontsize=9, color='#666666', ha='center', fontfamily='monospace')

    # Thin progress bar
    progress = route_idx / max(n_frames_ig - 1, 1)
    bar_y = 0.12
    ax_top_ig.fill_between([0.05, 0.95], [bar_y, bar_y], [bar_y + 0.06, bar_y + 0.06],
                           color='#2a2a2a', zorder=1)
    ax_top_ig.fill_between([0.05, 0.05 + 0.90 * progress], [bar_y, bar_y],
                           [bar_y + 0.06, bar_y + 0.06], color='#ffaa00', alpha=0.9, zorder=2)

    # Bottom panel - Instagram style
    ax_bot_ig.clear()
    ax_bot_ig.set_facecolor('#1e1e1e')
    ax_bot_ig.set_xlim(0, 1)
    ax_bot_ig.set_ylim(0, 1)
    ax_bot_ig.axis('off')

    ax_bot_ig.text(0.5, 0.92, wp[0].upper(), fontsize=14, fontweight='bold',
                   color='#ffffff', ha='center', fontfamily='monospace')
    ax_bot_ig.text(0.5, 0.82, f"\U0001f4c5 {wp[3]}", fontsize=10, color='#ffaa00',
                   ha='center', fontfamily='monospace')

    ax_bot_ig.plot([0.12, 0.88], [0.76, 0.76], color='#333333', linewidth=0.8)

    desc_lines = wp[4].split('\n')
    for i, line in enumerate(desc_lines):
        ax_bot_ig.text(0.5, 0.67 - i * 0.09, line, fontsize=9, color='#cccccc',
                       ha='center', fontfamily='monospace')

    ax_bot_ig.plot([0.12, 0.88], [0.45, 0.45], color='#333333', linewidth=0.8)

    ships, crew, note = get_fleet_status(wp_idx)
    ship_str = "\u26f5" * ships + "  \u2620" * (5 - ships)
    ax_bot_ig.text(0.5, 0.36, ship_str, fontsize=16, ha='center', color='#cccccc')
    ax_bot_ig.text(0.5, 0.24, f"{ships}/5 ships  \u00b7  ~{crew}/270 crew",
                   fontsize=8, color='#888888', ha='center', fontfamily='monospace')

    if wp_idx < 11:
        cmd = "\u2694\ufe0f Ferdinand Magellan"
        cmd_c = '#ffaa00'
    else:
        cmd = "\u2694\ufe0f Juan Sebasti\u00e1n Elcano"
        cmd_c = '#66bbff'
    ax_bot_ig.text(0.5, 0.12, cmd, fontsize=9, color=cmd_c,
                   ha='center', fontfamily='monospace', fontweight='bold')
    ax_bot_ig.text(0.5, 0.03, note, fontsize=7, color='#ff6b35',
                   ha='center', fontfamily='monospace', style='italic')

    return []

interval_ms_ig = int(1000 / target_fps_ig)
anim_ig = animation.FuncAnimation(fig_ig, animate_ig, frames=total_ig_frames,
                                   interval=interval_ms_ig, blit=False, repeat=True)

plt.close(fig_ig)
print(f"Instagram Reels animation: {total_ig_frames} frames at {target_fps_ig}fps")
print(f"Duration: ~{total_ig_frames / target_fps_ig:.1f} seconds")
print(f"Format: 9:16 vertical (1080x1920 at 180dpi)")
print(f"Route speed: {speed_ig:.2f} route points per frame")
print("Rendering HTML5 video...")

# %%
HTML(anim_ig.to_html5_video())

# %% [markdown]
# ## Static Overview: Key Moments of the Expedition
# #
# Let's also create a static multi-panel view showing the globe at key moments.
# 
# 

# %%
key_moments = [0, 3, 6, 9, 11, 14, 17, 18]
key_labels = [
    "Departure\nSep 1519",
    "Brazil\nDec 1519", 
    "Strait of Magellan\nOct 1520",
    "Guam\nMar 1521",
    "Magellan Killed\nApr 1521",
    "Spice Islands\nNov 1521",
    "Cape Verde\nJul 1522",
    "Return to Spain\nSep 1522"
]

fig2, axes = plt.subplots(2, 4, figsize=(18, 10), facecolor='#1e1e1e')
fig2.suptitle("MAGELLAN'S EXPEDITION \u2014 KEY MOMENTS",
              fontsize=18, fontweight='bold', color='#ffaa00', 
              fontfamily='monospace', y=0.98)

for idx, (ax, wp_idx, label) in enumerate(zip(axes.flat, key_moments, key_labels)):
    wp = waypoints[wp_idx]
    center_lat = wp[1] * 0.3
    center_lon = wp[2]
    route_idx = min(wp_idx * points_per_seg, n_frames - 1)

    draw_globe(ax, center_lat, center_lon, route_idx,
               continents_dict, smooth_lats, smooth_lons,
               waypoints, route_lats, route_lons)

    ax.text(0, -1.3, label, fontsize=9, color='#cccccc', ha='center',
            fontfamily='monospace', fontweight='bold')
    ax.text(-1.25, 1.15, f"{idx+1}", fontsize=14, fontweight='bold',
            color='#ffaa00', ha='center', fontfamily='monospace',
            bbox=dict(boxstyle='circle', facecolor='#333333', edgecolor='#ffaa00', linewidth=1.5))

plt.tight_layout(rect=[0, 0.02, 1, 0.95])
plt.savefig('magellan_key_moments.png', dpi=150, facecolor='#1e1e1e', 
            bbox_inches='tight', pad_inches=0.3)
plt.show()
print("Static overview saved!")

# %% [markdown]
# ## Expedition Statistics
# #
# A visual summary of the human cost and achievements of the expedition.
# 
# 

# %%
fig3, axes3 = plt.subplots(1, 3, figsize=(16, 5), facecolor='#1e1e1e')

# --- Panel 1: Crew survival ---
ax = axes3[0]
ax.set_facecolor('#1e1e1e')
categories = ['Departed', 'Survived']
values = [270, 18]
colors = ['#ff6b35', '#ffaa00']
bars = ax.bar(categories, values, color=colors, edgecolor='#ffffff', linewidth=0.5, width=0.5)
ax.set_ylabel('Number of Men', color='#cccccc', fontfamily='monospace')
ax.set_title('CREW', color='#ffaa00', fontfamily='monospace', fontweight='bold', fontsize=14)
ax.tick_params(colors='#888888')
ax.spines['bottom'].set_color('#444444')
ax.spines['left'].set_color('#444444')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
for bar, val in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
            str(val), ha='center', color='#ffffff', fontweight='bold',
            fontfamily='monospace', fontsize=14)
ax.text(0.5, 0.5, f"Survival rate:\n{18/270*100:.1f}%", transform=ax.transAxes,
        fontsize=12, color='#ff4444', ha='center', fontfamily='monospace',
        fontweight='bold')

# --- Panel 2: Ships timeline ---
ax = axes3[1]
ax.set_facecolor('#1e1e1e')
ship_names = ['Trinidad', 'San Antonio', 'Concepción', 'Victoria', 'Santiago']
ship_fates = ['Captured\nMoluccas 1522', 'Deserted\nAtlantic 1520', 
              'Burned\nPhilippines 1521', '✓ Completed\nvoyage!', 'Wrecked\nPatagonia 1520']
ship_durations = [36, 14, 24, 36, 8]  # months active
fate_colors = ['#ff4444', '#ff8844', '#ff4444', '#00cc66', '#ff4444']

bars = ax.barh(ship_names, ship_durations, color=fate_colors, edgecolor='#ffffff',
               linewidth=0.5, height=0.6, alpha=0.8)
ax.set_xlabel('Months Active', color='#cccccc', fontfamily='monospace')
ax.set_title('SHIPS', color='#ffaa00', fontfamily='monospace', fontweight='bold', fontsize=14)
ax.tick_params(colors='#888888')
ax.spines['bottom'].set_color('#444444')
ax.spines['left'].set_color('#444444')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
for bar, fate in zip(bars, ship_fates):
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
            fate, va='center', color='#cccccc', fontsize=7, fontfamily='monospace')
ax.set_xlim(0, 50)

# --- Panel 3: Distance / Time ---
ax = axes3[2]
ax.set_facecolor('#1e1e1e')

# Approximate distances for each leg
legs = ['Atlantic\nCrossing', 'South\nAmerica', 'Strait of\nMagellan', 
        'Pacific\nCrossing', 'Philippines\n& Spice Is.', 'Indian &\nAtlantic']
distances = [6000, 4000, 600, 12600, 3000, 14000]  # nautical miles approx
leg_colors = ['#3388ff', '#33aa55', '#ff6b35', '#ff4444', '#ffaa00', '#66bbff']

bars = ax.bar(legs, distances, color=leg_colors, edgecolor='#ffffff', linewidth=0.5, width=0.7)
ax.set_ylabel('Nautical Miles (approx)', color='#cccccc', fontfamily='monospace')
ax.set_title('DISTANCES', color='#ffaa00', fontfamily='monospace', fontweight='bold', fontsize=14)
ax.tick_params(colors='#888888', labelsize=7)
ax.spines['bottom'].set_color('#444444')
ax.spines['left'].set_color('#444444')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
for bar, val in zip(bars, distances):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 200,
            f"{val:,}", ha='center', color='#ffffff', fontsize=7,
            fontfamily='monospace', fontweight='bold')

total_nm = sum(distances)
ax.text(0.5, 0.85, f"Total: ~{total_nm:,} nm\n(~{total_nm*1.852:,.0f} km)",
        transform=ax.transAxes, fontsize=10, color='#ffaa00', ha='center',
        fontfamily='monospace', fontweight='bold')

plt.tight_layout()
plt.savefig('magellan_statistics.png', dpi=150, facecolor='#1e1e1e',
            bbox_inches='tight', pad_inches=0.3)
plt.show()



# %% [markdown]
# ## Timeline of Key Events
# #
# A visual timeline of the expedition's most important moments.
# 
# 

# %%
fig4, ax4 = plt.subplots(figsize=(16, 6), facecolor='#1e1e1e')
ax4.set_facecolor('#1e1e1e')

events = [
    ("Sep 1519", "Departure from\nSanlúcar de Barrameda", '#ffaa00', 1),
    ("Dec 1519", "Arrival at\nRio de Janeiro", '#3388ff', -1),
    ("Mar 1520", "Mutiny at\nPuerto San Julián", '#ff4444', 1),
    ("Oct 1520", "Discovery of the\nStrait of Magellan", '#00cc66', -1),
    ("Nov 1520", "Entry into the\nPacific Ocean", '#66bbff', 1),
    ("Mar 1521", "Landfall at\nGuam", '#ffaa00', -1),
    ("Apr 1521", "⚔️ Magellan killed\nat Battle of Mactan", '#ff0000', 1),
    ("Nov 1521", "🌿 Arrival at the\nSpice Islands", '#00cc66', -1),
    ("Feb 1522", "Victoria departs\nwest under Elcano", '#66bbff', 1),
    ("Sep 1522", "🏆 Return to Spain\n18 survivors", '#ffd700', -1),
]

# Timeline axis
x_positions = np.linspace(0.05, 0.95, len(events))

# Draw timeline line
ax4.plot([0.02, 0.98], [0.5, 0.5], color='#444444', linewidth=2, zorder=1)

for i, (date, desc, color, direction) in enumerate(events):
    x = x_positions[i]
    y_text = 0.5 + direction * 0.35
    y_mid = 0.5 + direction * 0.08
    
    # Vertical connector
    ax4.plot([x, x], [0.5, y_mid], color=color, linewidth=1.5, zorder=2)
    
    # Dot on timeline
    ax4.plot(x, 0.5, 'o', color=color, markersize=10, zorder=3,
             markeredgecolor='#ffffff', markeredgewidth=1)
    
    # Date
    ax4.text(x, y_mid + direction * 0.02, date, fontsize=8, color=color,
             ha='center', va='center' if direction > 0 else 'center',
             fontfamily='monospace', fontweight='bold')
    
    # Description
    ax4.text(x, y_text, desc, fontsize=7, color='#cccccc',
             ha='center', va='center', fontfamily='monospace',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#2a2a2a',
                       edgecolor=color, alpha=0.9, linewidth=1))

ax4.set_xlim(0, 1)
ax4.set_ylim(0, 1)
ax4.axis('off')
ax4.set_title("TIMELINE OF MAGELLAN'S EXPEDITION (1519-1522)",
              color='#ffaa00', fontfamily='monospace', fontweight='bold',
              fontsize=14, pad=20)

plt.tight_layout()
plt.savefig('magellan_timeline.png', dpi=150, facecolor='#1e1e1e',
            bbox_inches='tight', pad_inches=0.3)
plt.show()

print("\n" + "="*60)
print("  MAGELLAN'S EXPEDITION VISUALIZATION COMPLETE")
print("="*60)
print(f"\n  📊 Animation: {total_anim_frames} frames of globe rotation")
print(f"  🗺️  Route: {len(waypoints)} waypoints across {total_nm:,} nautical miles")
print(f"  ⛵ Ships: 5 departed, 1 returned")
print(f"  👥 Crew: 270 departed, 18 survived ({18/270*100:.1f}%)")
print(f"  📅 Duration: Sep 1519 – Sep 1522 (≈3 years)")
print(f"\n  Ferdinand Magellan (c.1480 – 27 April 1521)")
print(f"  Born: Northern Portugal")
print(f"  Died: Battle of Mactan, Philippines")
print(f"  Legacy: First circumnavigation of Earth")
print("="*60)



