# services/rss_service.py

import os
from datetime import datetime
from xml.etree import ElementTree as ET
from rich.console import Console
from rich.progress import Progress
from utils.logger import logger

console = Console()

RSS_FEED_PATH = os.path.join("github", "neurodeamon-feeds", "cursos.xml")

def _create_rss_element(parent, tag, text=None, attrib=None):
    """Cria um elemento XML e o anexa a um pai."""
    element = ET.SubElement(parent, tag, attrib=attrib if attrib else {})
    if text is not None:
        element.text = str(text)
    return element

def _get_or_create_channel(root):
    """Obtém ou cria o elemento <channel> no RSS feed."""
    channel = root.find('channel')
    if channel is None:
        channel = ET.SubElement(root, 'channel')
        _create_rss_element(channel, 'title', 'NeuroDeamon Courses')
        _create_rss_element(channel, 'link', 'https://github.com/emmanuelcandido/neurod') # Link do seu repositório
        _create_rss_element(channel, 'description', 'Podcasts gerados automaticamente a partir de cursos em vídeo.')
        _create_rss_element(channel, 'language', 'pt-br')
        _create_rss_element(channel, 'lastBuildDate', datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z'))
        _create_rss_element(channel, 'itunes:author', 'NeuroDeamon', attrib={'xmlns:itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd'})
        _create_rss_element(channel, 'itunes:summary', 'Podcasts gerados automaticamente a partir de cursos em vídeo.')
        _create_rss_element(channel, 'itunes:explicit', 'no')
        _create_rss_element(channel, 'itunes:image', attrib={'href': 'https://example.com/podcast_cover.jpg'}) # Imagem de capa do podcast
        _create_rss_element(channel, 'itunes:category', attrib={'text': 'Education'})
    return channel

def update_rss_feed(course_data: dict, progress: Progress = None, task_id = None) -> (bool, str):
    """Atualiza o arquivo RSS com os dados de um novo curso/episódio."""
    if not os.path.exists(os.path.dirname(RSS_FEED_PATH)):
        os.makedirs(os.path.dirname(RSS_FEED_PATH), exist_ok=True)

    try:
        if os.path.exists(RSS_FEED_PATH):
            tree = ET.parse(RSS_FEED_PATH)
            root = tree.getroot()
        else:
            root = ET.Element('rss', version='2.0', attrib={'xmlns:itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd'})
            tree = ET.ElementTree(root)
        
        channel = _get_or_create_channel(root)

        # Verifica se o item já existe para evitar duplicatas
        existing_item = None
        for item in channel.findall('item'):
            if item.find('guid').text == course_data['guid']:
                existing_item = item
                break

        if existing_item is not None:
            item = existing_item
            logger.info(f"Updating existing RSS item for {course_data['title']}")
            console.print(f"[bright_yellow]Updating existing RSS item for {course_data['title']}[/]")
        else:
            item = ET.SubElement(channel, 'item')
            logger.info(f"Adding new RSS item for {course_data['title']}")
            console.print(f"[bright_green]Adding new RSS item for {course_data['title']}[/]")

        _create_rss_element(item, 'title', course_data['title'])
        _create_rss_element(item, 'link', course_data['link'])
        _create_rss_element(item, 'guid', course_data['guid'])
        _create_rss_element(item, 'description', course_data['description'])
        _create_rss_element(item, 'pubDate', datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z'))
        _create_rss_element(item, 'enclosure', attrib={'url': course_data['enclosure_url'], 'length': course_data['enclosure_length'], 'type': 'audio/mpeg'})
        _create_rss_element(item, 'itunes:author', course_data.get('author', 'NeuroDeamon'))
        _create_rss_element(item, 'itunes:duration', course_data.get('duration', '00:00'))
        _create_rss_element(item, 'itunes:explicit', 'no')
        _create_rss_element(item, 'itunes:summary', course_data['description'])

        # Atualiza a data de construção do feed
        channel.find('lastBuildDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')

        tree.write(RSS_FEED_PATH, encoding='utf-8', xml_declaration=True)

        if progress and task_id is not None:
            progress.update(task_id, completed=100, description="RSS feed updated.")

        logger.info(f"RSS feed updated: {RSS_FEED_PATH}")
        return True, RSS_FEED_PATH
    except Exception as e:
        logger.error(f"Error updating RSS feed: {e}")
        return False, f"Error updating RSS feed: {e}"

# Exemplo de uso (para testes)
if __name__ == "__main__":
    async def main_test():
        dummy_course_data = {
            'title': 'Introdução à Neurociência',
            'link': 'https://example.com/neurociencia_podcast.mp3',
            'guid': 'neurociencia_podcast_123',
            'description': 'Um podcast sobre os fundamentos da neurociência.',
            'enclosure_url': 'https://example.com/neurociencia_podcast.mp3',
            'enclosure_length': '12345678', # Tamanho do arquivo em bytes
            'duration': '01:30:00',
            'author': 'Dr. Neuro',
        }

        console.print(f"[bold bright_blue]Starting RSS feed update...[/]")
        success, result = update_rss_feed(dummy_course_data)
        if success:
            console.print(f"[bright_green]RSS feed updated: {result}[/]")
        else:
            console.print(f"[bright_red]Error:[/]{result}")

        # Limpar arquivo dummy
        # if os.path.exists(RSS_FEED_PATH):
        #     os.remove(RSS_FEED_PATH)

    import asyncio
    asyncio.run(main_test())
