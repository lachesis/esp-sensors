try:
    import sunlight
except ImportError:
    pass
else:
    sunlight.main()

try:
    import weatherstation
except ImportError:
    pass
else:
    weatherstation.main()
