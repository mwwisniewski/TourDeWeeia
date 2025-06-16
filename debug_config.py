import pygame
from config import RED, GREEN, BLUE, YELLOW

def draw_debug_rect(surface, rect, color, camera_ofset, zoom, width=2):
    view_x = rect.x * zoom - camera_ofset.x
    view_y = rect.y * zoom - camera_ofset.y
    view_w = rect.width * zoom
    view_h = rect.height * zoom
    pygame.draw.rect(surface, color, pygame.Rect(view_x, view_y, view_w, view_h), width)

def draw_debug_visuals(surface, game_map, current_target_room, camera_offset, zoom):
    for zone in game_map.transition_zones:
        draw_debug_rect(surface, zone.rect, RED, camera_offset, zoom, width=2)

    for room in game_map.target_rooms:
        color = GREEN if room == current_target_room else BLUE
        draw_debug_rect(surface, room.rect, color, camera_offset, zoom, width=2)

    for named_zone_item in game_map.named_zones:
        draw_debug_rect(surface, named_zone_item.rect, YELLOW, camera_offset, zoom, width=1)


def log_player_transition(player_id_str, zone_name, target_position):
    print(f"[{player_id_str} PRZEJSCIE TEST] {zone_name} -> {target_position}")


def log_player_goal_arrival(game_instance, player, player_id_str):
    if game_instance.printed_arrived is False:
        if game_instance.current_target_room and game_instance.current_target_room.rect.colliderect(player.rect):
            print(f"[{player_id_str}] TRAFIL DO SALI: {game_instance.current_target_room.name}")
            game_instance.printed_arrived = True
            return True
    return False
