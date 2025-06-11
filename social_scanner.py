import requests
import json
import argparse
from concurrent.futures import ThreadPoolExecutor
from colorama import init, Fore, Style

# تهيئة الألوان
init()

# قائمة المواقع المدعومة
SOCIAL_SITES = {
    'Facebook': 'https://www.facebook.com/{}',
    'Twitter': 'https://twitter.com/{}',
    'Instagram': 'https://www.instagram.com/{}',
    'GitHub': 'https://github.com/{}',
    'LinkedIn': 'https://www.linkedin.com/in/{}',
    'Pinterest': 'https://www.pinterest.com/{}',
    'Reddit': 'https://www.reddit.com/user/{}',
    'YouTube': 'https://www.youtube.com/@{}',
    'TikTok': 'https://www.tiktok.com/@{}',
    'Snapchat': 'https://www.snapchat.com/add/{}',
    'Medium': 'https://medium.com/@{}',
    'DeviantArt': 'https://www.deviantart.com/{}',
    'Twitch': 'https://www.twitch.tv/{}',
    'Telegram': 'https://t.me/{}',
    'Behance': 'https://www.behance.net/{}'
}

def check_username(site_name, site_url, username):
    """فحص اسم المستخدم في موقع معين"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        url = site_url.format(username)
        response = requests.get(url, headers=headers, timeout=5)

        if response.status_code == 200:
            return {
                'site': site_name,
                'url': url,
                'exists': True,
                'status_code': response.status_code
            }
        elif response.status_code == 404:
            return {
                'site': site_name,
                'url': url,
                'exists': False,
                'status_code': response.status_code
            }
        else:
            return {
                'site': site_name,
                'url': url,
                'exists': None,
                'status_code': response.status_code
            }
    except Exception as e:
        return {
            'site': site_name,
            'url': site_url.format(username),
            'exists': None,
            'error': str(e)
        }

def search_username(username):
    """البحث عن اسم المستخدم في جميع المواقع المدعومة"""
    results = []
    
    print(f"\n{Fore.CYAN}جاري البحث عن اسم المستخدم: {username}{Style.RESET_ALL}\n")
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_site = {executor.submit(check_username, site_name, site_url, username): site_name 
                         for site_name, site_url in SOCIAL_SITES.items()}
        
        for future in future_to_site:
            result = future.result()
            results.append(result)
            
            # طباعة النتيجة بالألوان
            if result.get('exists') is True:
                print(f"{Fore.GREEN}[+] {result['site']}: {result['url']}{Style.RESET_ALL}")
            elif result.get('exists') is False:
                print(f"{Fore.RED}[-] {result['site']}: غير موجود{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}[?] {result['site']}: غير متأكد{Style.RESET_ALL}")
    
    return results

def save_results(results, username):
    """حفظ النتائج في ملف JSON"""
    filename = f"{username}_social_media.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n{Fore.CYAN}تم حفظ النتائج في الملف: {filename}{Style.RESET_ALL}")

def main():
    parser = argparse.ArgumentParser(description='البحث عن اسم المستخدم في مواقع التواصل الاجتماعي')
    parser.add_argument('username', help='اسم المستخدم المراد البحث عنه')
    args = parser.parse_args()

    results = search_username(args.username)
    save_results(results, args.username)

if __name__ == '__main__':
    main()
