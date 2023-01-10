%% Script to find all relevant indices of A50%% Find the index of all relevant events: A500s and T500s

% The script is used to find "true adaptation" with the A500 adaptors 
% (when two tones of the same frequency follow each other close in time, i.e., 
% A500 - T500 pairs of the same 500Hz frequency). 

%% Load eeglab and the file
% call eeglab (make sure to navigate to the eeglab folder)
eeglab

%% Set up paths
in_datadir  = '/Volumes/New Volume/ica_interpolated'; % on Mac
out_datadir = '/Users/stojanovic/Documents/Projects/Cambridge/Analyses/Adaptor/NewEEGFilesAdaptor';

addpath(in_datadir);
addpath(out_datadir);

%% Subject lists
   
sub = {'02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12',...
       '13', '14', '15', '16', '17', '19', '20', '21', '23', '24', '25',...
       '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36',...
       '37', '38'};


%% Find the index of all relevant events: A500s and T500s

% First, create event lists for all relevant events (A500 and T500 combined), then only
% A500, and only T500.

sleepeventsAT500all = {'N2A500_0','N2A500_1', 'N2A500_2', 'N2A500_3', 'N2A500_4',...
                     'N3A500_0','N3A500_1', 'N3A500_2', 'N3A500_3', 'N3A500_4',...
                     'RpA500_0','RpA500_1', 'RpA500_2', 'RpA500_3', 'RpA500_4',...
                     'RtA500_0','RtA500_1', 'RtA500_2', 'RtA500_3', 'RtA500_4',...
                     'N2T500_0','N2T500_1', 'N2T500_2', 'N2T500_3', 'N2T500_4',...
                     'N3T500_0','N3T500_1', 'N3T500_2', 'N3T500_3', 'N3T500_4',...
                     'RpT500_0','RpT500_1', 'RpT500_2', 'RpT500_3', 'RpT500_4',...
                     'RtT500_0','RtT500_1', 'RtT500_2', 'RtT500_3', 'RtT500_4'};
                 
sleepeventsA500     = {'N2A500_0','N2A500_1', 'N2A500_2', 'N2A500_3', 'N2A500_4',...
                     'N3A500_0','N3A500_1', 'N3A500_2', 'N3A500_3', 'N3A500_4',...
                     'RpA500_0','RpA500_1', 'RpA500_2', 'RpA500_3', 'RpA500_4',...
                     'RtA500_0','RtA500_1', 'RtA500_2', 'RtA500_3', 'RtA500_4'};
                   
sleepeventsT500     = {'N2T500_0','N2T500_1', 'N2T500_2', 'N2T500_3', 'N2T500_4',...
                     'N3T500_0','N3T500_1', 'N3T500_2', 'N3T500_3', 'N3T500_4',...
                     'RpT500_0','RpT500_1', 'RpT500_2', 'RpT500_3', 'RpT500_4',...
                     'RtT500_0','RtT500_1', 'RtT500_2', 'RtT500_3', 'RtT500_4'};

%% Find and select events

% First, find all the event names in the EEG structure.
allevents = {EEG.event.type};

% Create empty vectors to store events. the vectors give number indices 
% indicating the time points of the A500 and T500 events.
selectALLevents  = []; % list of all (both A- and T500) events 
selectA500events = []; % list of all A500 events
selectT500events = []; % list of all T500 events

% Select events from complete list in sleep.
for e = 1:length(sleepeventsAT500all)
    selectALLevents = [selectALLevents find(strncmp(sleepeventsAT500all{e},allevents,length(sleepeventsAT500all{e})))];
end

% Sort the events to make sure we always have an A500 before T500. 
sortedALLevents = sort(selectALLevents);

% Select A500 events from complete list in sleep.
for e = 1:length(sleepeventsA500)
    selectA500events = [selectA500events find(strncmp(sleepeventsA500{e},allevents,length(sleepeventsA500{e})))];
end

% Select T500 events from complete list in sleep.
for e = 1:length(sleepeventsT500)
    selectT500events = [selectT500events find(strncmp(sleepeventsT500{e},allevents,length(sleepeventsT500{e})))];
end

%% Find A500 before T500

% find the locations of T500 in the vector of all events.
[ind,loc_T500] = intersect(sortedALLevents,selectT500events);

% Verify that the event before the location of the first T500 is an A500.
onebeforeT500  = (loc_T500 - 1);
onebeforeT500events = {EEG.event(sortedALLevents(onebeforeT500)).type};

% Verify that these are unique events in the list.
eventtype_beforeT500 = unique(onebeforeT500events);

%% Remove undesired T500 events

% undesired_eventtypes now returns the T500 tones in the list that we do not want. 
undesired_eventtypes = setdiff(eventtype_beforeT500,eventlistA500);

% Sleep 
% undesired_eventtypes = setdiff(eventtype_beforeT500,sleepeventsA500);

if ~isempty(undesired_eventtypes) % if the cell 'undesired_eventtypes' isn't empty, 
    % create empty vector for data to be deleted
    tbd = []; % 'to be delected' vector
    for i = 1:length(undesired_eventtypes) % loop over the undesired events (T500s)
        tbd = [tbd find(strcmp(undesired_eventtypes(i),onebeforeT500events))];
    end

% New variable - time points of A500s before T500.
A500stimepoints      = onebeforeT500;
A500stimepoints(tbd) = []; % returns the locations of the T500 undesired events
end

% Now check in the EEG data struct there are only A500_0 - A500_4 events.
A500sevents      = {EEG.event(sortedALLevents(A500stimepoints)).type};
A500sevents      = unique(A500sevents); % now should return only A500 events without
                                        % the undesired T500 events

%% Check T500 events

% Check all T500 events.
T500sevents      = {EEG.event(sortedALLevents(onebeforeT500) + 1).type};
T500sevents      = unique(T500sevents);

% Make sure that T500s only contain the T500 events.
% This step can be skipped in case there are no anomalies in the cell.

undesired_eventtypes = setdiff(T500sevents,eventlistT500); % if other events/undesired events exist,
                                                           % use set diff to find and exclude them

if ~isempty(undesired_eventtypes) % if the cell isn't empty, i.e., there are undesired T events,
    tbd = [];     % create empty vector for data to be deleted
    for i = 1:length(undesired_Teventtypes) % loop over the undesired events (undesired tones)
        % find undesired events in the list 
        tbd = [tbd find(strcmp(undesired_eventtypes(i),checkT500events))]; % to exclude
    end

% Create new variable without these undesired tones, so leaving only
% desired T500 events.
desiredT500stimepoints      = T500sevents;
desiredT500stimepoints(tbd) = []; % the locations of the T500 undesired events
else 
    desiredT500stimepoints  = T500sevents;
end                                       

%% Check the location(s) of the values, i.e., where we know there is a T500

A500sevents = sortedALLevents(onebeforeT500);
T500sevents = sortedALLevents(loc_T500);

%% Index the desired data

events = [EEG.epoch.event]';
A = ismember(events,A500sevents);
a = find(A == 1);

T = ismember(events,T500sevents);
% T = events(a - 1);
t = find(T == 1);

% T500s
for e = 1:length(t)
    if strcmp(EEG.epoch(t(e)).eventtype(1:4),'N2T500')
        EEG.epoch(t(e)).eventtype = [EEG.epoch(t(e)).eventtype '_bT'];
    end
end

% Sleep A500s
for e = 1:length(a)
% check that the event type is indeed one of the A500s
     if strcmp(EEG.epoch(a(e)).eventtype(1:4),'N2A500') % change based on sleep state, for N2, N3, and REM
         EEG.epoch(a(e)).eventtype = [EEG.epoch(a(e)).eventtype '_bT'];
     end
end 

% Sleep T500s
for e = 1:length(t)
    if strcmp(EEG.epoch(t(e)).eventtype(1:4),'N2T500')
        EEG.epoch(t(e)).eventtype = [EEG.epoch(t(e)).eventtype '_bT'];
    end
end

%% Save EEG

% Navigate to the desired folder where to save the files manually. 
% Might have to add data per subject manually as well.

% Save the .set file per subject. Change name based on subject name.
save -mat EEG_32_wake.set EEG

% Save the .fdt file per subject.
data = EEG;
data = 'EEG_32_wake.fdt';
floatwrite(data(:,:)', 'EEG_32_wake.fdt'); 
