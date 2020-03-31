
# Post
        # Пинг интерфейсных плат
        if PING == True:
            # Цикл опроса диапазонов 
            bands = ['D2', 'D3', 'D4', 'D5']
            for band in bands:
            
                if band == 'D2':
                # Настройка на требуемую частоту приема Д2 , при помощи отладочного пакета управления РПУ 0х8А
                elif band == 'D3':             
                elif band == 'D4':
                elif band == 'D5':
                else:
                    pass

                while True:
                    # формируем буфер                    
                    # проверка посылки на длительность
                    if len(data) == 488:                        
                    elif len(data) == 1448:                        
                    else:
                        continue                 
                    # деление посылки на отрезки по 8 каналов
                    data = [data[i:i + 8] for i in range(0, len(data), 8)]

                    # поиск максимальной амплитуды в кассетах ЦОС
                    max_lst = [i.index(max(i)) + 1 for i in data]
                    # поиск совпадений с эталонным массивом
                    if band == 'D2':
                    # Для каждого диапазона свой эталон
                    elif band == 'D3':
                    elif band == 'D4':
                    elif band == 'D5':
                    else:
                        continue
                    
                    # В массиве comparison содержиться информация о каждом МШУ текущего диапазона (здесь подкрышивается ячейка)
                    for i in comparison:                      
                        if band == 'D2':                         
                        elif band == 'D3':                            
                        elif band == 'D4':                            
                        elif band == 'D5':                            
                        else:
                            pass
                    break
        else:
            print('Not connection')
