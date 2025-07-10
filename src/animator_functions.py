import random
from colorama import Fore, Style
from src.engine.dat import Vector2

def clear(c, layer):
    c.clear_layer(layer)

def noise(c, layer, amount, chars, colours):
    for n in range(amount):
        location = Vector2(random.randint(0, c.dimensions.x - 1), random.randint(0, c.dimensions.y - 1))
        c.set_char(
            layer, location, random.choice(chars), random.choice(colours)
        )

def cluster_noise(c, layer, num_clusters, points_per_cluster, spread, chars, colours):
    """
    Creates tight clusters of noise characters on the screen.
    
    Args:
        c: Canvas to draw on
        layer: Layer to draw on
        num_clusters: Number of cluster centers
        points_per_cluster: How many points to generate around each cluster
        spread: Maximum distance from cluster centers (1 = very tight, 2 = loose)
        chars: List of characters to choose from
        colours: List of colors to choose from
    """
    # Generate cluster centers with better spacing
    centers = []
    for _ in range(num_clusters):
        center_x = random.randint(spread + 2, c.dimensions.x - spread - 3)
        center_y = random.randint(spread + 2, c.dimensions.y - spread - 3)
        centers.append((center_x, center_y))
    
    # Generate points around each center with tighter distribution
    for center_x, center_y in centers:
        for _ in range(points_per_cluster):
            # For very tight clusters, bias towards center positions
            if spread == 1:
                # 70% chance for center or immediately adjacent (8 directions)
                if random.random() < 0.7:
                    offsets = [(0,0), (-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
                    x_offset, y_offset = random.choice(offsets)
                else:
                    # 30% chance for slightly further (still within spread=1)
                    x_offset = random.randint(-1, 1)
                    y_offset = random.randint(-1, 1)
            else:
                # For larger spreads, use uniform distribution but weighted towards center
                if random.random() < 0.5:
                    # 50% chance for positions closer to center
                    max_offset = max(1, spread // 2)
                    x_offset = random.randint(-max_offset, max_offset)
                    y_offset = random.randint(-max_offset, max_offset)
                else:
                    # 50% chance for full spread
                    x_offset = random.randint(-spread, spread)
                    y_offset = random.randint(-spread, spread)
            
            x = center_x + x_offset
            y = center_y + y_offset
            
            # Ensure points stay within canvas bounds
            x = max(0, min(x, c.dimensions.x - 1))
            y = max(0, min(y, c.dimensions.y - 1))
            
            location = Vector2(x, y)
            c.set_char(
                layer, location, random.choice(chars), random.choice(colours)
            )


def expanding_cluster_noise(c, layer, center_x, center_y, expansion_radius, chars, colours):
    """
    Adds one character per frame, expanding outward from center.
    Call this each frame with increasing expansion_radius for expanding effect.
    
    Args:
        c: Canvas to draw on
        layer: Layer to draw on
        center_x: X coordinate of cluster center
        center_y: Y coordinate of cluster center  
        expansion_radius: Current expansion radius (0=center, 1=adjacent, etc.)
        chars: List of characters to choose from
        colours: List of colors to choose from
    """
    if expansion_radius == 0:
        # Place center point
        location = Vector2(center_x, center_y)
        c.set_char(layer, location, random.choice(chars), random.choice(colours))
        return
    
    # Generate all possible positions at this radius
    possible_positions = []
    for x_offset in range(-expansion_radius, expansion_radius + 1):
        for y_offset in range(-expansion_radius, expansion_radius + 1):
            # Only include positions that are exactly at this distance (Manhattan or Chebyshev)
            distance = max(abs(x_offset), abs(y_offset))  # Chebyshev distance for square expansion
            # distance = abs(x_offset) + abs(y_offset)  # Manhattan distance for diamond expansion
            
            if distance == expansion_radius:
                x = center_x + x_offset
                y = center_y + y_offset
                
                # Check bounds
                if 0 <= x < c.dimensions.x and 0 <= y < c.dimensions.y:
                    possible_positions.append((x, y))
    
    # Place one random character at this expansion radius
    if possible_positions:
        x, y = random.choice(possible_positions)
        location = Vector2(x, y)
        c.set_char(layer, location, random.choice(chars), random.choice(colours))


def cluster_expansion_single(c, layer, cluster_centers, current_radius, chars, colours):
    """
    Expands multiple clusters simultaneously, one character per frame total.
    
    Args:
        c: Canvas to draw on
        layer: Layer to draw on
        cluster_centers: List of (x, y) tuples for cluster centers
        current_radius: Current expansion radius for all clusters
        chars: List of characters to choose from
        colours: List of colors to choose from
    """
    # Collect all possible positions from all clusters at current radius
    all_positions = []
    
    for center_x, center_y in cluster_centers:
        if current_radius == 0:
            # Center position
            if 0 <= center_x < c.dimensions.x and 0 <= center_y < c.dimensions.y:
                all_positions.append((center_x, center_y))
        else:
            # Positions at current radius
            for x_offset in range(-current_radius, current_radius + 1):
                for y_offset in range(-current_radius, current_radius + 1):
                    distance = max(abs(x_offset), abs(y_offset))  # Square expansion
                    
                    if distance == current_radius:
                        x = center_x + x_offset
                        y = center_y + y_offset
                        
                        if 0 <= x < c.dimensions.x and 0 <= y < c.dimensions.y:
                            all_positions.append((x, y))
    
    # Place one character from all possible positions
    if all_positions:
        x, y = random.choice(all_positions)
        location = Vector2(x, y)
        c.set_char(layer, location, random.choice(chars), random.choice(colours))



def type_text(c, generator, layer, x, y, col, render=True):
    # pop a char off the manager's text if there is one
    text_get = generator.get_data("text")
    offset = generator.get_data("offset")
    total_chars = 0
    add_offset = 0
    if text_get:
        if text_get.startswith("[##CLEAR|"):
            clear_bounds = text_get.split("|")[1].split(";")
            for yclear in range(int(clear_bounds[1])):
                location = Vector2(x, y + yclear)

                if render:
                    c.set_string(
                        layer, location, " " * int(clear_bounds[0]), col
                    )
        else:
            for linecount, text_line in enumerate(text_get.split("\n")):
                local_offset = offset - total_chars
                if 0 <= local_offset < len(text_get):
                    place_typer = local_offset < len(text_line) - 1
                    string = text_line[:local_offset] + ("_" if place_typer else "")
                    if local_offset < len(text_line) and text_line[local_offset] == "@":
                        add_offset += 3

                    string = string.replace("~", "").replace("@", "")
                    total_chars += len(text_line)
                    location = Vector2(x, y + linecount)

                    if render:
                        c.set_string(
                            layer, location, string, col
                        )

            generator.oper_data("offset", lambda t: t + 1 + add_offset)


def set_multiline_string(c, layer, x, y, string, col):
    for offset, line in enumerate(string.split("\n")):
        c.set_string(
            layer, Vector2(x, y + offset), line, col
        ),

def debug_info(c, g, b, frames):
    c.set_string(
        0, Vector2(32, 1), "{:4} g | {:4} l".format(g.parent.cur_beat, g.parent.active_scene[0].internal_beat), Style.BRIGHT + Fore.YELLOW
    ),
    counted_scenes = 0
    for index, scene in enumerate(filter(lambda s: s.name != "debug_counter", g.parent.active_scene)):
        c.set_string(
            0, Vector2(32, index + 2), "{:^17}".format(
                scene.name + " ({})".format(len(list(filter(lambda g: g.start_beat <= b, scene.generators))))
            ), Style.NORMAL + Fore.GREEN
        ),

        counted_scenes += 1

    for index2 in range(counted_scenes, 6):
        c.set_string(
            0, Vector2(32, index2 + 2), "                 ", Style.NORMAL + Fore.GREEN
        ),

    c.set_string(
        0, Vector2(32, 8), "  {:4} e/s".format(c.edits_this_frame), Style.BRIGHT + Fore.YELLOW
    ),

    avg_differences = sum(frames[i] - frames[i - 1] for i in range(len(frames) - 1, 0, -1))
    if avg_differences:
        avg_differences /= 10
    else:
        avg_differences = 60

    c.set_string(
        0, Vector2(32, 9), " {:6} fps".format(round(1 / avg_differences, 1)), Style.BRIGHT + Fore.YELLOW
    ),

    cols = (
        Fore.BLACK,
        Fore.RED,
        Fore.GREEN,
        Fore.YELLOW,
        Fore.BLUE,
        Fore.MAGENTA,
        Fore.CYAN,
        Fore.WHITE,
    )

    styles = (
        Style.NORMAL,
        Style.BRIGHT
    )
    for index in range(16):
        c.set_char(
            0, Vector2(32 + (index % 8), 11 + (index // 8)), "##", cols[index % 8] + styles[index // 8]
        ),


def clear(c, layer):
    c.clear_layer(layer)


def typewrite_by_word(c, generator, layer, x, y, col, render=True, history_var="history"):
    # Show the text up to offset words at line lineno
    text_get = generator.get_data("text")
    offset = generator.get_data("offset")
    lineno = generator.get_data("lineno")
    if text_get:
        if lineno < len(text_get):
            line_get = text_get[lineno]
            line_total = "".join(line for line in line_get[:offset])

            if line_get and len(line_get) > 0:  # Make sure line_get has elements
                if isinstance(line_get[0], str) and line_get[0].startswith("[~~CLEAR|"):
                    clear_bounds = line_get[0].split("|")[1]
                    location = Vector2(x, y)

                    if render:
                        c.set_string(
                            layer, location, " " * int(clear_bounds), col
                        )
                else:
                    # print line_total and increment offset by 1.
                    # if offset is > lineno, reset offset and increment lineno
                    # if line_total is empty (offset == 0), print a clear
                    if render:
                        if line_total:
                            c.set_string(
                                layer, Vector2(x, y), line_total.replace("~", ""), col
                            ),
                        else:
                            c.set_string(
                                layer, Vector2(x, y), " " * 60, col
                            ),

                    if offset >= len(line_get):
                        history = generator.parent.get_data(history_var)
                        is_fluff = line_total.startswith(" ") or not line_total
                        is_important = line_total.endswith("~")
                        colour_select = Fore.YELLOW + Style.BRIGHT
                        prefix = "- "
                        if is_fluff:
                            prefix = "  "
                            colour_select = Fore.BLACK + Style.BRIGHT
                        elif is_important:
                            prefix = "> "
                            colour_select = Fore.GREEN + Style.BRIGHT

                        if not history:
                            history = [(
                                prefix + line_total.strip(" ").replace("~", ""), colour_select
                            )]
                            generator.parent.set_data(history_var, history)
                        else:
                            history.append((
                                prefix + line_total.strip(" ").replace("~", ""), colour_select
                            ))

                        generator.parent.set_data("refresh", True)

                        generator.set_data("offset", 0)
                        generator.set_data("lineno", lineno + 1)
                    else:
                        generator.set_data("offset", offset + 1)

            else:
                generator.set_data("offset", offset + 1)


def write_history(c, generator, layer, x, y, col, stop, var="history"):
    # Write history from y position going upwards until 0
    history = generator.parent.get_data(var)
    need_refresh = generator.parent.get_data("refresh")

    if need_refresh:
        generator.parent.set_data("refresh", False)

        if history:
            lineid = 0
            for ypos in range(y, stop - 1, -1):
                line = history[len(history) - 1 - lineid] if lineid < len(history) else ("", Fore.BLACK + Style.BRIGHT)
                lineid += 1

                location = Vector2(x, ypos)

                c.set_string(
                    layer, location, "{:50}".format(line[0]), line[1]
                ),
        else:
            for ypos in range(y, stop - 1, -1):
                c.set_string(
                    layer, Vector2(x, ypos), " " * 50, Fore.BLACK + Style.NORMAL
                ),