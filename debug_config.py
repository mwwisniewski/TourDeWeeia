import pygame
from config import RED, GREEN, BLUE, YELLOW


def draw_debug_visuals(surface, game_map, current_target_room, camera_offset, zoom):
    for zone in game_map.transition_zones:
        debug_rect_map = zone.rect.copy()
        view_x = debug_rect_map.x * zoom - camera_offset.x
        view_y = debug_rect_map.y * zoom - camera_offset.y
        view_w = debug_rect_map.width * zoom
        view_h = debug_rect_map.height * zoom
        rect_on_view = pygame.Rect(view_x, view_y, view_w, view_h)
        pygame.draw.rect(surface, RED, rect_on_view, 2)

    for room in game_map.target_rooms:
        debug_rect_map = room.rect.copy()
        view_x = debug_rect_map.x * zoom - camera_offset.x
        view_y = debug_rect_map.y * zoom - camera_offset.y
        view_w = debug_rect_map.width * zoom
        view_h = debug_rect_map.height * zoom
        rect_on_view = pygame.Rect(view_x, view_y, view_w, view_h)
        color = GREEN if room == current_target_room else BLUE
        pygame.draw.rect(surface, color, rect_on_view, 2)

    for named_zone_item in game_map.named_zones:
        debug_rect_map = named_zone_item.rect.copy()
        view_x = debug_rect_map.x * zoom - camera_offset.x
        view_y = debug_rect_map.y * zoom - camera_offset.y
        view_w = debug_rect_map.width * zoom
        view_h = debug_rect_map.height * zoom
        rect_on_view = pygame.Rect(view_x, view_y, view_w, view_h)
        pygame.draw.rect(surface, YELLOW, rect_on_view, 1)


def log_player_transition(player_id_str, zone_name, target_position):
    print(f"[{player_id_str} PRZEJSCIE TEST] {zone_name} -> {target_position}")


def log_player_goal_arrival(game_instance, player, player_id_str):
    if game_instance.printed_arrived is False:
        if game_instance.current_target_room and game_instance.current_target_room.rect.colliderect(player.rect):
            print(f"[{player_id_str}] TRAFIL DO SALI: {game_instance.current_target_room.name}")
            game_instance.printed_arrived = True
            return True
    return False
