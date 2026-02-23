    for site in sites:
                            if site in text:
                                speak(f"Opening {site} for you, Sir.")
                                webbrowser.open(sites[site])
                                break
                    