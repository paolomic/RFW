import utl

######################################################################################################
#  Dump - (Develop Helpers)
######################################################################################################
#region

def dump_uia_detail(item):
    properties = item.legacy_properties()
    print('### legacy_properties:')
    print(properties)

    props = item.get_properties()
    print('### get_properties:')
    print(props)

    try:
        wrapper = item.wrapper_object()
        print(wrapper.get_toggle_state())
    except:
        print("Toggle interface non disponibile")

    try:
        print(item.iface_toggle.CurrentToggleState())
    except:
        print("Toggle interface non disponibile")

    print('### dir(item):')
    print(dir(item))  # mostra tutti i metodi/proprietà disponibili


def dump_uia_item(element, level=0):
    """
    Converte un elemento UIA in una stringa formattata.
    
    Args:
        element: Elemento UIAWrapper da convertire
        level: Livello di indentazione
    Returns:
        str: Stringa formattata con le proprietà dell'elemento
    """
    try:
        indent = "  " * level
        
        # Raccolta proprietà
        visible = element.is_visible() if hasattr(element, 'is_visible') else None
        control_type = element.element_info.control_type if hasattr(element.element_info, 'control_type') else None
        class_name = element.element_info.class_name if hasattr(element.element_info, 'class_name') else None
        automation_id = element.element_info.automation_id if hasattr(element.element_info, 'automation_id') else None
        window_text = element.window_text() if hasattr(element, 'window_text') else None
        
        # Tentativo di estrarre texts dalle properties
        texts = []
        try:
            properties = element.get_properties()
            texts = properties.get('texts', [])
        except:
            pass
        
        # Costruzione parti dell'output
        output_parts = [
            f"{indent}Level={level}",
            f"Visible={visible}",
            f"Type={control_type}",
            f"Class={class_name}",
            f"AutomationId={automation_id}",
            f"Text='{window_text}'" if window_text else "Text=None",
            f"Texts={texts}" if texts else "Texts=[]"
        ]
        
        return " | ".join(output_parts)
        
    except Exception as e:
        return f"{indent}Error processing element: {str(e)}"

#@utl.chrono_function
def dump_uia_tree(element, level=0, max_depth=None, file_path='out.txt', first_call=True):
    """
    Stampa l'albero dei controlli su file, una riga per elemento.
    
    Args:
        element: Elemento UIAWrapper da analizzare
        level: Livello corrente di indentazione
        max_depth: Profondità massima dell'albero
        file_path: Percorso del file di output
        first_call: Flag per resettare il file alla prima chiamata
    """
    # Reset file if this is the first call
    mode = 'w' if first_call else 'a'
    
    try:
        with open(file_path, mode, encoding='utf-8') as f:
            # Dump elemento corrente
            f.write(dump_uia_item(element, level) + "\n")
            
            # Processo ricorsivo sui figli
            if max_depth is None or level < max_depth:
                try:
                    children = element.children()
                    for child in children:
                        dump_uia_tree(child, level + 1, max_depth, file_path, False)
                except Exception as e:
                    f.write(f"{'  ' * level}Error getting children: {str(e)}\n")
                    
    except Exception as e:
        print(f"Error writing to file: {str(e)}")


def refresh_uia_tree(element):
    try:
        xxx = dump_uia_item(element, 0) + "\n"
        try:
            children = element.children()
            for child in children:
                refresh_uia_tree(child)
        except Exception as e:
            pass
                    
    except Exception as e:
        print(f"Error writing to file: {str(e)}")

        
def dump_uia_path(item, root=None, file_path='out.txt'):
    """
    Stampa il percorso dall'elemento item fino al root (o alla window se root non specificato)
    risalendo con parent().
    
    Args:
        item: Elemento UIAWrapper di partenza
        root: Elemento UIAWrapper di arrivo (opzionale)
        file_path: Percorso del file di output
    """
    try:
        # Raccogli il percorso risalendo con parent()
        path = []
        current = item
        while current is not None:
            path.append(current)
            if root and current == root:
                break
            try:
                current = current.parent()
            except:
                break
                
        # Se root è specificato ma non è stato trovato nel percorso
        if root and path[-1] != root:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("Path not found: root element is not an ancestor of item\n")
            return
            
        # Inverti il path per averlo dal root al target
        path.reverse()
        
        # Scrivi il percorso su file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("=== Path from root to target ===\n")
            for level, element in enumerate(path):
                f.write(dump_uia_item(element, level) + "\n")
                
    except Exception as e:
        print(f"Error in dump_uia_path: {str(e)}")       
        

def dump_uia_detail(item, indent=""):
    """
    Funzione per analizzare e stampare tutti i dettagli disponibili di un elemento UIA
    Args:
        item: Elemento UIA da analizzare
        indent: Indentazione per output annidato (default "")
    """
    def print_section(title, indent=""):
        print(f"\n{indent}{'='*20} {title} {'='*20}")
    
    def safe_get(func, default="Non disponibile"):
        try:
            result = func()
            return result
        except Exception as e:
            return f"{default} (Errore: {str(e)})"
    
    # Informazioni base dell'elemento
    print_section("INFORMAZIONI BASE", indent)
    print(f"{indent}Elemento: {item}")
    print(f"{indent}Tipo: {type(item)}")
    
    # Element Info
    print_section("ELEMENT INFO", indent)
    if hasattr(item, 'element_info'):
        ei = item.element_info
        print(f"{indent}Control Type: {safe_get(lambda: ei.control_type)}")
        print(f"{indent}Class Name: {safe_get(lambda: ei.class_name)}")
        print(f"{indent}Name: {safe_get(lambda: ei.name)}")
        print(f"{indent}Handle: {safe_get(lambda: ei.handle)}")
        print(f"{indent}Runtime ID: {safe_get(lambda: ei.runtime_id)}")
        print(f"{indent}Rectangle: {safe_get(lambda: ei.rectangle)}")
        print(f"{indent}Process ID: {safe_get(lambda: ei.process_id)}")
    
    # Properties
    print_section("PROPERTIES", indent)
    print(f"{indent}Legacy Properties:")
    legacy_props = safe_get(lambda: item.legacy_properties())
    for key, value in legacy_props.items() if isinstance(legacy_props, dict) else []:
        print(f"{indent}  {key}: {value}")
    
    print(f"\n{indent}Get Properties:")
    props = safe_get(lambda: item.get_properties())
    for key, value in props.items() if isinstance(props, dict) else []:
        print(f"{indent}  {key}: {value}")
    
    # Stati e Toggle
    print_section("STATI E TOGGLE", indent)
    print(f"{indent}Toggle State: {safe_get(lambda: item.get_toggle_state())}")
    print(f"{indent}Is Selected: {safe_get(lambda: item.is_selected())}")
    print(f"{indent}Is Enabled: {safe_get(lambda: item.is_enabled())}")
    print(f"{indent}Is Visible: {safe_get(lambda: item.is_visible())}")
    
    # Pattern Interfaces
    print_section("PATTERN INTERFACES", indent)
    patterns = [
        'iface_toggle', 'iface_selection', 'iface_selection_item',
        'iface_value', 'iface_range_value', 'iface_grid', 'iface_table',
        'iface_text', 'iface_invoke', 'iface_expand_collapse'
    ]
    
    # Gestione sicura dei pattern
    for pattern in patterns:
        try:
            interface = getattr(item, pattern, None)
            if interface is not None:
                print(f"{indent}{pattern}: Disponibile")
                # Gestione sicura dei metodi specifici per pattern
                if pattern == 'iface_toggle':
                    print(f"{indent}  Toggle State: {safe_get(lambda: interface.CurrentToggleState())}")
                elif pattern == 'iface_value':
                    print(f"{indent}  Value: {safe_get(lambda: interface.CurrentValue())}")
        except Exception as e:
            print(f"{indent}{pattern}: Non disponibile (Errore: {str(e)})")
    
    # Metodi disponibili
    print_section("METODI DISPONIBILI", indent)
    methods = [method for method in dir(item) if not method.startswith('_')]
    print(f"{indent}Metodi totali: {len(methods)}")
    for method in sorted(methods):
        print(f"{indent}  {method}")

#endregion