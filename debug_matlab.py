import matlab.engine

future_eng = matlab.engine.start_matlab(background=True)
eng = future_eng.result()

env = eng.getenv() # Environmental variables
eng.disp(env,nargout=0) # Display environmental variables
eng. disp(license('inuse'),nargout=0) # Licenses in use